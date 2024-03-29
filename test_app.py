import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, db_drop_and_create_all

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""
    def setUp(self):
        # """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgresql://{}/{}".format('postgres:secret@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        db_drop_and_create_all()
        self.userToken = os.environ.get("userToken") 
        pass
    def tearDown(self):
        """Executed after each test"""
        print("teardown completed")
        pass
    
    #positive test case that GET actors works as expected
    def test_get_actors(self):
        response = self.client().get('/actors', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        print("test_get_actors started")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(bool(data['actors']), True)  #Asserts that 'actors' contains some data
    
    #negative test case that GET actors should not work when you try to GET a particular actor
    def test_405_requesting_particular_actor(self):
        print("test_requesting particular actor started")
        response = self.client().get('/actors/1', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    #positive test case that GET movies works as expected
    def test_get_movies(self):
        print("test_get_movies started")
        response = self.client().get('/movies', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(bool(data['movies']), True)  #Asserts that 'movies' contains some data
    
    #negative test case that GET movies should not work when you try to GET a particular movie
    def test_405_requesting_particular_movie(self):
        print("test_requesting particular movie started")
        response = self.client().get('/movies/1', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    #positive test case that DELETE actors works as expected
    def test_delete_actors(self):
        print("test_delete_actors started")
        response = self.client().delete('/actors/2', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        actor = Actor.query.filter(Actor.id == 2).one_or_none() #returns if the actor #2 exists or doesn't exist
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(actor, None) #confirms that actor #2 no longer exists (actor = None)

    #negative test case that DELETE actors should not work when you try to DELETE a non-existent actor
    def test_422_deleting_nonexistent_actor(self):
        print("test_delete nonexistent_actors started")
        response = self.client().delete('/actors/5000', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

  #positive test case that DELETE movies works as expected
    def test_delete_movies(self):
        print("test_delete movies started")
        response = self.client().delete('/movies/2', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        movie = Movie.query.filter(Movie.id == 2).one_or_none() #returns if the movie #2 exists or doesn't exist
        print(movie)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertEqual(movie, None) #confirms that movie #2 no longer exists (movie = None)

    #negative test case that DELETE movies should not work when you try to DELETE a non-existent movie
    def test_422_deleting_nonexistent_movie(self):
        print("test_delete nonexistent movie started")
        response = self.client().delete('/movies/5000', headers={"Authorization": f"Bearer {self.userToken}"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
  
    #positive test case that POST actors works as expected
    def test_post_actors(self):
        print("test_post_actors started")
        self.new_actor = {
            'name': 'Mark Zuckerberg',
            'age': '33',
            'gender': 'Male'
        }
        response = self.client().post('/actors', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(bool(data['created']), True)
        
    #negative test case that POST actors should not work when you try to POST to a particular actor ID
    def test_405_posting_to_particular_actor(self):
        print("test_posting particular_actor started")
        self.new_actor = {
            'name': 'Leo DiCaprio',
            'age': 50,
            'gender': 'Male'
        }
        response = self.client().post('/actors/1', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    #negative test case that POST actors should not work when you try to POST with blank values
    def test_422_posting_blank_actor(self):
        print("test_post_blank_actors started")
        self.blank_actor = {
            'name': '',
            'age': '',
            'gender': ''
        }
        response = self.client().post('/actors', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.blank_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    #positive test case that POST movies works as expected
    def test_post_movies(self):
        print("test_post_movies started")
        self.new_movie = {
            'title': 'Dune',
            'releasedate': '2022-01-31'
        }
        response = self.client().post('/movies', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(bool(data['created']), True)
        
    #negative test case that POST movies should not work when you try to POST to a particular movie ID
    def test_405_posting_to_particular_movie(self):
        print("test_psot partiocular movie started")
        self.new_movie = {
            'title': 'It Part II',
            'releasedate': '2022-02-14'
        }
        response = self.client().post('/movies/1', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    #negative test case that POST movies should not work when you try to POST with blank values
    def test_422_posting_blank_movie(self):
        print("test_post blank movie started")
        self.blank_movie = {
            'title': '',
            'releasedate': ''
        }
        response = self.client().post('/movies', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.blank_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    #positive test case that PATCH actors works as expected
    def test_patch_actors(self):
        print("test_patch_actors started")
        self.updated_actors = {
            'name': 'Barney Stinson',
            'age': 40,
            'gender': 'Male'
        }
        response = self.client().patch('/actors/3', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.updated_actors)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 3)

    #positive test case that PATCH movies works as expected
    def test_patch_movies(self):
        print("test_patch movies started")
        self.updated_movie = {
            'title': 'Barney',
            'releasedate': '2022-03-30'
        }
        response = self.client().patch('/movies/3', headers={"Authorization": f"Bearer {self.userToken}"}, json=self.updated_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 3)

# Make the tests conveniently executable
if __name__ == "__main__":
    print("executing tests")
    """Define test variables and initialize app."""
    unittest.main()