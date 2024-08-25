import unittest
from app import app
import json

class FlaskAppTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_get_all_cats_no_user_id(self):
        response = self.client.get('/cats')
        self.assertEqual(response.status_code, 400)
        self.assertIn('User ID is required', response.get_data(as_text=True))

    def test_get_all_cats_success(self):
        response = self.client.get('/cats?user_id=1&page=1&limit=2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('cats', data)
        self.assertIn('total_cats', data)

    def test_get_cat_by_id_not_found(self):
        response = self.client.get('/cats/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Cat not found', response.get_data(as_text=True))

    def test_add_cat_to_favorites_missing_data(self):
        response = self.client.post('/cats', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('User ID and Image ID are required', response.get_data(as_text=True))

    def test_add_cat_to_favorites_success(self):
        response = self.client.post('/cats', json={'user_id': 1, 'image_id': 'abc123', 'name': 'Persian', 'description': 'Friendly'})
        self.assertIn(response.status_code, [200, 201])
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Cat added to favorites successfully', data['message'])

    def test_delete_favorite_cat_not_found(self):
        response = self.client.delete('/cats?user_id=1&image_id=nonexistent_id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Favorite cat not found', response.get_data(as_text=True))

    def test_delete_favorite_cat_success(self):
        # Assuming a cat with ID 'abc123' exists in user 1's favorites
        response = self.client.delete('/cats?user_id=1&image_id=abc123')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Favorite cat successfully removed', response.get_data(as_text=True))

    def test_update_breed_no_fields_to_update(self):
        response = self.client.put('/cats/1', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No fields to update', response.get_data(as_text=True))

    def test_update_breed_success(self):
        # Assuming a cat with ID 'abc123' exists
        response = self.client.put('/cats/abc123', json={'name': 'New Name', 'description': 'New Description'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Breed updated successfully', response.get_data(as_text=True))

    def test_get_favorite_cats_no_user_id(self):
        response = self.client.get('/cats/favorite')
        self.assertEqual(response.status_code, 400)
        self.assertIn('User ID is required', response.get_data(as_text=True))

    def test_get_favorite_cats_success(self):
        response = self.client.get('/cats/favorite?user_id=1&page=1&limit=2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('cats', data)
        self.assertIn('total_cats', data)

if __name__ == '__main__':
    unittest.main()



