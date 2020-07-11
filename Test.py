import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON
from flask import jsonify

from app import *
from API import *
from Models import *

class AskyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, database_path)

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_question(self):
        res = self.client().get('/questions/26')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['content'], "how are you sersy?")
        self.assertTrue(data['success'])
        self.assertGreater(data['total_categories'],0)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
