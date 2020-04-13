import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
import configparser

config = configparser.ConfigParser()
config.read_file(open(r'..\..\config\config.ini'))
USERNAME = config.get('postgres','username')
PASSWORD = config.get('postgres','password')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgres://'+USERNAME+':'+PASSWORD+'@localhost:5432/trivia'
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question': 'what is udacity',
            'answer': 'offers MOOCS',
            'difficulty': 1,
            'category': 1
        }
    
        self.search_term = {
            'searchTerm': 'actor'
        }

        self.no_search_term = {
            'searchTerm': 'who is applejack'
        }

        self.quiz_category = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass  
   
    def test_get_all_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(response.status_code, 200)
    
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])      
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(response.status_code, 200)

    def test_404_sent_requesting_beyond_valid_page(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data.decode('utf-8'))
        question = Question.query.filter(Question.id == 1).one_or_none()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(question, None)

    def test_create_questions(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_422_if_question_creation_fails(self):
        response = self.client().post('/books', json=self.new_question)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_question_search_with_results(self):
        response = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_question_search_without_results(self):
        response = self.client().post('/books', json=self.no_search_term)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        

    def test_get_questions_by_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(data['questions']), 0)

    def test_get_questions_by_invalid_category(self):
        response = self.client().get('/categories/11/questions')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_play_quiz_questions(self):
        response = self.client().post('/quizzes', json=self.quiz_category)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']) 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()