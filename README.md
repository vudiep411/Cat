# Fun Fullstack Cat Application
This is a fun Cat application that interacts with TheCatAPI to retrieve information about 100 random cats, including their images, and allows users to perform create, read, update, and delete (CRUD) operations on this data within a local application.

## Installation
Follow these steps to set up this application locally. Make sure to have [Docker](https://www.docker.com/) installed and set up environment variable in `.env` file similar to [.env.example](.env.example)

### Set up Postgres Database
1. Go into postgres directory
    ```
    cd postgres
    ```
2. Run the script to initialize postgres database with docker and insert data.
   ```
   ./script.bat
   ```

   > Note: this script set default username and password to `admin` feel free to modify it.
   Now postgres database will run at localhost:5438

### Set up backend
1. Go in backend directory
    ```
    cd backend
    ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Run the service
    ```
    python app.py
    ```

> API documentation can be found after running the service at http://localhost:8080/apidocs

### Set up front end
1. CD into frontend
   ```
   cd fronend
   ```
2. Install dependencies
   ```
   npm install
   ```
3. Run the service
   ```
   npm run dev
   ```
> Front end application is now running at http://localhost:5000/
> 
> Note: This is a SPA (Single Page Application) design so there is only 1 route

### Set up Flask with Docker
    ```
    docker build -t flask-cat-app .
    docker run -d -p 8080:8080 flask-cat-app
    ```


## API Endpoints
### Retrieve All Cats
* Endpoint: GET /cats
  
* Description: Retrieves paginated cat information from the database with optional filters for breed and search queries.

* Sample Response:

    ```json
    {
        "current_page": 1,
        "total_pages": 3,
        "total_cats": 25,
        "cats": [
            {
            "id": "cat_id",
            "image_url": "http://example.com/cat.jpg",
            "breed_name": "Persian",
            "weight": "4-5 kg",
            "temperament": "Gentle",
            "origin": "Iran",
            "description": "Long-haired breed of cat",
            "life_span": "12-17 years",
            "indoor": 1,
            "adaptability": 4,
            "affection_level": 5,
            "child_friendly": 3,
            "dog_friendly": 4,
            "energy_level": 2,
            "grooming": 5,
            "intelligence": 3,
            "social_needs": 3,
            "stranger_friendly": 2,
            "favorite": true
            }
        ]
    }
    ```

* Sample Usage:
  ```
  curl -X GET "http://localhost:8080/cats?user_id=1&page=1&limit=10&breed=Persian&query=gentle"
  ```

### Add Cat to Favorites
* Endpoint: POST /cats
* Add a cat to the user's favorites.
* Sample response:
  ```json
  {
    "message": "Cat added to favorites successfully"
  }
  ```
* Sample Usage:
  ```bash
  curl -X POST "http://localhost:8080/cats" \
    -H "Content-Type: application/json" \
    -d '{
    "user_id": 1,
    "image_id": "cat_id",
    "name": "Persian",
    "description": "Long-haired breed of cat"
    }'
  ```

### Delete Favorite Cat
* Endpoint: DELETE /cats

* Delete a cat from the user's favorites.

* Query Parameters:
    * user_id (required): The user's ID.
    * image_id (required): The image ID of the cat.
* Sample Response:
    ```json
    {
        "message": "Favorite cat successfully removed"
    }
    ```
* Sample usage:
    ```bash
    curl -X DELETE "http://localhost:8080/cats?user_id=1&image_id=cat_id"
    ```

### Get Cat by ID
* Endpoint: GET /cats/{id}
* Retrieve specific cat details by cat ID.
* Path Parameters:
    * id (required): The ID of the cat.
  
* Response:
    ```json
    {
        "id": "cat_id",
        "image_url": "http://example.com/cat.jpg",
        "breed": {
            "id": "breed_id",
            "name": "Persian",
            "weight": "4-5 kg",
            "temperament": "Gentle",
            "origin": "Iran",
            "description": "Long-haired breed of cat",
            "life_span": "12-17 years",
            "indoor": 1,
            "adaptability": 4,
            "affection_level": 5,
            "child_friendly": 3,
            "dog_friendly": 4,
            "energy_level": 2,
            "grooming": 5,
            "intelligence": 3,
            "social_needs": 3,
            "stranger_friendly": 2
        }
    }
    ```
* Usage:
    ```bash
    curl -X GET "http://localhost:8080/cats/cat_id"
    ```

### Update Breed Information
* Endpoint: PUT /cats/{id}

* Update the breed information (name or description) for a specific cat.

* Path Parameters:

    * id (required): The ID of the cat.
* Request Body:
    ```json
    {
        "name": "Siamese",
        "description": "Sleek, vocal breed of cat"
    }
    ```
* Response:
    ```json
    {
        "message": "Breed updated successfully"
    }
    ```
* Usage:
  ```bash
    curl -X PUT "http://localhost:8080/cats/cat_id" \
        -H "Content-Type: application/json" \
        -d '{
        "name": "Siamese",
        "description": "Sleek, vocal breed of cat"
    }'

  ```

### Get Favorite Cats
* Endpoint: GET /cats/favorite

* Retrieve a user's favorite cat images.

* Query Parameters:

    * user_id (required): The user's ID.
    * page (optional): Page number (default: 1).
    * limit (optional): Number of results per page (default: 10).
  
* Response:
  ```json
  {
    "current_page": 1,
    "total_pages": 1,
    "total_cats": 5,
    "cats": [{
        "id": "cat_id",
        "image_url": "http://example.com/cat.jpg",
        "breed_name": "Persian",
        "weight": "4-5 kg",
        "temperament": "Gentle",
        "origin": "Iran",
        "description": "Long-haired breed of cat",
        "life_span": "12-17 years",
        "indoor": 1,
        "adaptability": 4,
        "affection_level": 5,
        "child_friendly": 3,
        "dog_friendly": 4,
        "energy_level": 2,
        "grooming": 5,
        "intelligence": 3,
        "social_needs": 3,
        "stranger_friendly": 2,
        "favorite": true
        }]
    }
  ```
* Example Usage
  ```bash
  curl -X GET "http://localhost:8080/cats/favorite?user_id=1&page=1&limit=10"
  ```