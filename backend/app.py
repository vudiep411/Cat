from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from dotenv import load_dotenv
import psycopg2
import os
from swagger_config import get_swagger_config 
from flask_cors import CORS 

load_dotenv()

app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template=get_swagger_config())

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DEV = os.environ.get('DEV')

def get_db_connection():
    connection = psycopg2.connect(
        database=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        host="localhost" if DEV == "1" else "postgres", 
        port=5438 if DEV == "1" else 5432
    )
    return connection


@app.route('/cats', methods=['GET'])
def get_all_cats():
    """Retrieve paginated cat information from the database with optional breed and search query."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('limit', 10))
    breed = request.args.get('breed')
    search_query = request.args.get('query', '')  # New parameter for search query
    conn = get_db_connection()
    cursor = conn.cursor()

    # Base query
    base_query = """
        SELECT ci.id, ci.image_url, b.name AS breed_name, b.weight, b.temperament, b.origin, b.description, b.life_span, 
               b.indoor, b.adaptability, b.affection_level, b.child_friendly, b.dog_friendly, b.energy_level, 
               b.grooming, b.intelligence, b.social_needs, b.stranger_friendly, up.id AS user_preference_id,
               CASE WHEN up.image_id IS NOT NULL THEN TRUE ELSE FALSE END AS favorite
        FROM cat_images ci
        JOIN breeds b ON ci.breed_id = b.id
        LEFT JOIN user_preferences up ON ci.id = up.image_id AND up.user_id = %s
        WHERE 1=1
    """
    
    # Add breed filter if provided
    if breed:
        base_query += " AND LOWER(b.name) LIKE LOWER(%s)"
    
    # Add search query filter if provided
    if search_query:
        base_query += " AND LOWER(b.description) LIKE LOWER(%s)"
    
    # Add pagination
    base_query += " LIMIT %s OFFSET %s"
    
    # Get total count of cats
    count_query = """
        SELECT COUNT(*)
        FROM cat_images ci
        JOIN breeds b ON ci.breed_id = b.id
        LEFT JOIN user_preferences up ON ci.id = up.image_id AND up.user_id = %s
        WHERE 1=1
    """
    
    # Add breed filter to count query if provided
    if breed:
        count_query += " AND LOWER(b.name) LIKE LOWER(%s)"
    
    # Add search query filter to count query if provided
    if search_query:
        count_query += " AND LOWER(b.description) LIKE LOWER(%s)"
    
    # Execute count query
    count_params = (user_id,)
    if breed:
        count_params += (f'%{breed.lower()}%',)
    if search_query:
        count_params += (f'%{search_query.lower()}%',)
    
    cursor.execute(count_query, count_params)
    total_cats = cursor.fetchone()[0]

    # Calculate pagination parameters
    offset = (page - 1) * per_page
    total_pages = (total_cats + per_page - 1) // per_page  # Ceiling division

    # Retrieve cats for the current page
    search_params = (user_id,)
    if breed:
        search_params += (f'%{breed.lower()}%',)
    if search_query:
        search_params += (f'%{search_query.lower()}%',)
    
    cursor.execute(base_query, search_params + (per_page, offset))
    cats = cursor.fetchall()

    col_names = [desc[0] for desc in cursor.description]
    cat_list = [dict(zip(col_names, cat)) for cat in cats]

    cursor.close()
    conn.close()

    # Return paginated data
    return jsonify({
        'current_page': page,
        'total_pages': total_pages,
        'total_cats': total_cats,
        'cats': cat_list
    })


@app.route('/cats', methods=['POST'])
def add_cat_to_favorites():
    """Add a cat to the user's favorites."""
    data = request.get_json()

    user_id = data.get('user_id')
    image_id = data.get('image_id')
    name = data.get('name')
    description = data.get('description')

    if not user_id or not image_id:
        return jsonify({'message': 'User ID and Image ID are required'}), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'message': 'User ID must be an integer'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if the favorite already exists
        cursor.execute("""
            SELECT id FROM user_preferences WHERE user_id = %s AND image_id = %s
        """, (user_id, image_id))
        
        existing_favorite = cursor.fetchone()
        
        if existing_favorite:
            return jsonify({'message': 'Favorite already exists'}), 409

        # Insert into user_preferences table
        cursor.execute("""
            INSERT INTO user_preferences (user_id, image_id, name, description)
            VALUES (%s, %s, %s, %s)
            RETURNING id
            """, (user_id, image_id, name, description))
        new_id = cursor.fetchone()[0]
        conn.commit()
        message = 'Cat added to favorites successfully'
    except Exception as e:
        conn.rollback()
        message = f'An error occurred: {str(e)}'
    finally:
        cursor.close()
        conn.close()

    return jsonify({'message': message, 'id': new_id}), 201


@app.route('/cats/<int:id>', methods=['DELETE'])
def delete_favorite_cat(id):
    """Delete a cat from user favorites by its ID."""
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the favorite exists
    cursor.execute("""
        SELECT * FROM user_preferences WHERE id = %s
    """, (id,))
    favorite = cursor.fetchone()

    if favorite is None:
        cursor.close()
        conn.close()
        return jsonify({"error": "Favorite cat not found"}), 404

    # Delete the favorite
    cursor.execute("""
        DELETE FROM user_preferences WHERE id = %s
    """, (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": "Favorite cat successfully removed",
        "id": id
    }), 200


@app.route('/cats/<string:id>', methods=['GET'])
def get_cat_by_id(id):
    """Retrieve a specific cat's details."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ci.id, ci.image_url, b.*
        FROM cat_images ci
        JOIN breeds b ON ci.breed_id = b.id
        WHERE ci.id = %s
    """, (id,))
    
    cat = cursor.fetchone()
    cursor.close()
    conn.close()

    if cat is None:
        return jsonify({'message': 'Cat not found'}), 404

    # Extracting all breed attributes
    breed_attributes = {
        'id': cat[2],
        'name': cat[3],
        'weight': cat[4],
        'temperament': cat[5],
        'origin': cat[6],
        'description': cat[7],
        'life_span': cat[8],
        'indoor': cat[9],
        'adaptability': cat[10],
        'affection_level': cat[11],
        'child_friendly': cat[12],
        'dog_friendly': cat[13],
        'energy_level': cat[14],
        'grooming': cat[15],
        'intelligence': cat[16],
        'social_needs': cat[17],
        'stranger_friendly': cat[18]
    }

    cat_details = {
        'id': cat[0],
        'image_url': cat[1],
        'breed': breed_attributes
    }

    return jsonify(cat_details), 200


@app.route('/cats/<id>', methods=['PUT'])
def update_breed(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    query_parts = []
    values = []

    for field in ['name', 'description']:
        if field in data:
            query_parts.append(f"{field} = %s")
            values.append(data[field])
    
    if not query_parts:
        return jsonify({'message': 'No fields to update'}), 400
    
    values.append(id)
    query = f"""
        UPDATE user_preferences
        SET {', '.join(query_parts)}
        WHERE id = %s
    """

    cursor.execute(query, tuple(values))
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Not found'}), 404

    return jsonify({'message': 'Breed updated successfully'}), 200


@app.route('/cats/favorite', methods=['GET'])
def get_favorite_cats():
    """Retrieve a user's favorite cat images."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('limit', 10))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Base query for favorites
    base_query = """
        SELECT ci.id, ci.image_url, up.name AS breed_name, b.weight, b.temperament, b.origin, up.description, b.life_span, 
               b.indoor, b.adaptability, b.affection_level, b.child_friendly, b.dog_friendly, b.energy_level, 
               b.grooming, b.intelligence, b.social_needs, b.stranger_friendly, up.id AS user_preference_id,
               TRUE AS favorite
        FROM user_preferences up
        JOIN cat_images ci ON up.image_id = ci.id
        JOIN breeds b ON ci.breed_id = b.id
        WHERE up.user_id = %s
    """

    # Add pagination
    base_query += " LIMIT %s OFFSET %s"
    
    # Get total count of favorite cats
    count_query = """
        SELECT COUNT(*)
        FROM user_preferences up
        JOIN cat_images ci ON up.image_id = ci.id
        JOIN breeds b ON ci.breed_id = b.id
        WHERE up.user_id = %s
    """
    
    cursor.execute(count_query, (user_id,))
    total_cats = cursor.fetchone()[0]

    # Calculate pagination parameters
    offset = (page - 1) * per_page
    total_pages = (total_cats + per_page - 1) // per_page  # Ceiling division

    # Retrieve favorite cats for the current page
    cursor.execute(base_query, (user_id, per_page, offset))
    favorites = cursor.fetchall()

    col_names = [desc[0] for desc in cursor.description]
    favorite_list = [dict(zip(col_names, favorite)) for favorite in favorites]
    cursor.close()
    conn.close()

    # Return paginated data
    return jsonify({
        'current_page': page,
        'total_pages': total_pages,
        'total_cats': total_cats,
        'cats': favorite_list
    })


if __name__ == '__main__':
    if DEV == "1":
        app.run(debug=True, port=8080)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)