import unittest
import json
from flask import jsonify
from app import create_app
from decouple import config
import os

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case with 19 test case"""

    def setUp(self):
        self.database_path = config('DATABASE_PATH')
        self.app = create_app(self.database_path)
        self.client = self.app.test_client()
        self.manager_token = os.environ.get('manager_token')
        self.staff_token = os.environ.get('staff_token')

    def tearDown(self):
        """Executed after each test"""
        pass
    
    def test_get_actors_without_token(self):
        """Test GET /actors endpoint"""

        response = self.client.get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_get_actors(self):
        """Test GET /actors endpoint"""

        response = self.client.get('/actors', headers={
            'Authorization': "Bearer {}".format(self.staff_token)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)

    def test_get_actor_by_id(self):
        """Test GET /actors/<int:actor_id> endpoint"""
        # Assume actor_id is a valid ID
        actor_id = 2

        response = self.client.get(f'/actors/{actor_id}', headers={
            'Authorization': "Bearer {}".format(self.staff_token)
        })
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['actor'])
    
    def test_get_actor_by_id_without_token(self):
        """Test GET /actors/<int:actor_id> endpoint"""
        # Assume actor_id is a valid ID
        actor_id = 1

        response = self.client.get(f'/actors/{actor_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 401)

    def test_create_actor_success_with_manager_token(self):
        """Test POST /actors endpoint (success)"""
        actor_data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male',
            'bio': 'Some bio',
            'nationality': 'US',
            'profile_image': 'https://example.com/profile.jpg',
            'movie_ids': [1, 2, 3]  # List of movie IDs
        }

        response = self.client.post('/actors',
                                    json=actor_data,
                                    headers={'Authorization': f'Bearer {self.manager_token}'})

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['created'])

    def test_create_actor_fail_with_staff_token(self):
        """Test POST /actors endpoint (success)"""
        actor_data = {
            'name': 'John Doe',
            'age': 30,
            'gender': 'Male',
            'bio': 'Some bio',
            'nationality': 'US',
            'profile_image': 'https://example.com/profile.jpg',
            'movie_ids': [1, 2, 3]  # List of movie IDs
        }

        response = self.client.post('/actors',
                                    json=actor_data,
                                    headers={'Authorization': f'Bearer {self.staff_token}'})

        data = response.get_json()

        self.assertEqual(response.status_code, 401)

    def test_update_actor_success_manager(self):
        """Test PATCH /actors/<actor_id> endpoint (success with manager token)"""
        actor_id = 2
        actor_data = {
            'name': 'Updated Name',
            'age': 40,
            'gender': 'Female',
            'bio': 'Updated bio',
            'nationality': 'US',
            'profile_image': 'https://example.com/profile.jpg',
            'movie_ids': [1, 2, 3]  # List of movie IDs
        }

        response = self.client.patch(f'/actors/{actor_id}',
                                    json=actor_data,
                                    headers={'Authorization': f'Bearer {self.manager_token}'})

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['actor_info'])

    def test_update_actor_failure_staff(self):
        """Test PATCH /actors/<actor_id> endpoint (failure with staff token)"""
        actor_id = 15
        actor_data = {
            'name': 'Updated Name',
            'age': 40,
            'gender': 'Female',
            'bio': 'Updated bio',
            'nationality': 'US',
            'profile_image': 'https://example.com/profile.jpg',
        }

        response = self.client.patch(f'/actors/{actor_id}',
                                    json=actor_data,
                                    headers={'Authorization': f'Bearer {self.staff_token}'})

        self.assertEqual(response.status_code, 401)

    def test_delete_actor_success(self):
        """Test DELETE /actors/<actor_id> endpoint with valid token"""
        actor_id = 15  # ID of the actor to be deleted

        # Perform the delete request with the manager token
        response = self.client.delete(f'/actors/{actor_id}', headers={
            'Authorization': f'Bearer {self.manager_token}'
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_actor_id'], actor_id)

    def test_delete_actor_failure(self):
        """Test DELETE /actors/<actor_id> endpoint with invalid token"""
        actor_id = 5  # ID of the actor to be deleted

        # Perform the delete request with the staff token
        response = self.client.delete(f'/actors/{actor_id}', headers={
            'Authorization': f'Bearer {self.staff_token}'
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Unauthorized')

    # movie test ***********************


    def test_get_movies_success(self):
        """Test GET /movies endpoint"""

        response = self.client.get('/movies', headers={
            'Authorization': f'Bearer {self.manager_token}'
        })

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
    
    def test_get_movies_success_without_token(self):

        response = self.client.get('/movies')

        data = response.get_json()

        self.assertEqual(response.status_code, 401)


    def test_create_movie_success(self):

        movie_data = {
            "title": "Movie 1",
            "release_date": "2022-01-01",
            "description": "A great movie",
            "genre": "Action",
            "director": "John Doe",
            "poster_image": "https://example.com/poster.jpg",
            "average_rating": 4.5,
        }

        response = self.client.post('/movies', headers={
            'Authorization': f'Bearer {self.manager_token}'
        }, json=movie_data)

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertIsNotNone(data.get('created'))

    def test_create_movie_unauthorized(self):

        movie_data = {
            "title": "Movie 1",
            "release_date": "2022-01-01",
            "description": "A great movie",
            "genre": "Action",
            "director": "John Doe",
            "poster_image": "https://example.com/poster.jpg",
            "average_rating": 4.5,
        }

        response = self.client.post('/movies', headers={
            'Authorization': f'Bearer {self.staff_token}'
        }, json=movie_data)

        self.assertEqual(response.status_code, 401)

    def test_get_movie_by_id(self):
        movie_id = 2

        response = self.client.get(f'/movies/{movie_id}', headers={
            'Authorization': f'Bearer {self.manager_token}'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('movie', data)
        self.assertIsInstance(data['movie'], dict)
        self.assertIn('title', data['movie'])
        self.assertIn('release_date', data['movie'])

    def test_update_movie_success(self):
        movie_id = 2  
        new_title = "Updated Title"

        response = self.client.patch(f'/movies/{movie_id}', headers={
            'Authorization': f'Bearer {self.manager_token}'
        }, json={
            'title': new_title
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('movie_info', data)
        self.assertIsInstance(data['movie_info'], dict)
        self.assertEqual(data['movie_info']['title'], new_title)

    def test_update_movie_failure(self):

        movie_id = 2 

        response = self.client.patch(f'/movies/{movie_id}', headers={
            'Authorization': f'Bearer {self.staff_token}'
        }, json={
            'title': "Updated Title"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_delete_movie_success(self):

        movie_id = 1

        response = self.client.delete(f'/movies/{movie_id}', headers={
            'Authorization': f'Bearer {self.manager_token}'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('deleted_movie_id', data)
        self.assertEqual(data['deleted_movie_id'], movie_id)

    def test_delete_movie_failure(self):
        movie_id = 1


        response = self.client.delete(f'/movies/{movie_id}', headers={
            'Authorization': f'Bearer {self.staff_token}'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Unauthorized')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
