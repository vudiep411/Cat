import psycopg2
import os
from dotenv import load_dotenv
import requests

load_dotenv()

CAT_API_KEY = os.getenv("CAT_API_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to postgres
connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host="localhost", port=5438)
cursor = connection.cursor()

# Create tables
CREATE_USER_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);
"""

CREATE_USER_PREFERENCES_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    image_id VARCHAR(255),
    name VARCHAR(255),
    description VARCHAR(1024),
    UNIQUE(user_id, image_id)
)
"""

CREATE_CAT_IMAGE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS cat_images (
    id VARCHAR(255) PRIMARY KEY,
    image_url VARCHAR(255) NOT NULL,
    breed_id VARCHAR(255) NOT NULL
);
"""

CREATE_BREEDS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS breeds (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    weight VARCHAR(255) NOT NULL,
    temperament VARCHAR(255) NOT NULL,
    origin VARCHAR(255) NOT NULL,
    description VARCHAR(1024) NOT NULL,
    life_span VARCHAR(255) NOT NULL,
    indoor INTEGER NOT NULL,
    adaptability INTEGER NOT NULL,
    affection_level INTEGER NOT NULL,
    child_friendly INTEGER NOT NULL,
    dog_friendly INTEGER NOT NULL,
    energy_level INTEGER NOT NULL,
    grooming INTEGER NOT NULL,
    intelligence INTEGER NOT NULL,
    social_needs INTEGER NOT NULL,
    stranger_friendly INTEGER NOT NULL
)
"""

# Create tables
cursor.execute(CREATE_USER_TABLE_QUERY)
cursor.execute(CREATE_USER_PREFERENCES_TABLE_QUERY)
cursor.execute(CREATE_CAT_IMAGE_TABLE_QUERY)
cursor.execute(CREATE_BREEDS_TABLE_QUERY)

connection.commit()

# Get all breeds
res = requests.get("https://api.thecatapi.com/v1/breeds")
breed_data = res.json()

for breed in breed_data:
    id = breed["id"]
    name = breed["name"]
    weight = breed.get("weight", {}).get("metric", "")
    temperament = breed.get("temperament", "")
    origin = breed.get("origin", "")
    description = breed.get("description", "")
    life_span = breed.get("life_span", "")
    indoor = breed.get("indoor", 0)  # Default to 0 if not present
    adaptability = breed.get("adaptability", 0)  # Default to 0 if not present
    affection_level = breed.get("affection_level", 0)  # Default to 0 if not present
    child_friendly = breed.get("child_friendly", 0)  # Default to 0 if not present
    dog_friendly = breed.get("dog_friendly", 0)  # Default to 0 if not present
    energy_level = breed.get("energy_level", 0)  # Default to 0 if not present
    grooming = breed.get("grooming", 0)  # Default to 0 if not present
    intelligence = breed.get("intelligence", 0)  # Default to 0 if not present
    social_needs = breed.get("social_needs", 0)  # Default to 0 if not present
    stranger_friendly = breed.get("stranger_friendly", 0)  # Default to 0 if not present

    cursor.execute("""
        INSERT INTO breeds (id, name, weight, temperament, origin, description, life_span, indoor, adaptability, affection_level, child_friendly, dog_friendly, energy_level, grooming, intelligence, social_needs, stranger_friendly)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (id, name, weight, temperament, origin, description, life_span, indoor, adaptability, affection_level, child_friendly, dog_friendly, energy_level, grooming, intelligence, social_needs, stranger_friendly))

    connection.commit()

# Get 100 cats
res = requests.get(f"https://api.thecatapi.com/v1/images/search?limit=100&api_key={CAT_API_KEY}&has_breeds=1")
data = res.json()
for cat in data:
    info = cat["breeds"][0]

    id = cat["id"]
    image_url = cat["url"]
    breed_id = info["id"]

    cursor.execute("""
        INSERT INTO cat_images (id, image_url, breed_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (id, image_url, breed_id))
    connection.commit()

cursor.close()
connection.close()

