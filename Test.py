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

    # ======= Get Question ============
    def test_get_question(self):
        res = self.client().get('/questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['question']['content'], "test_question")
        self.assertEqual(data['question']['user_id'], 25)
    def testFail_get_question(self):
        res = self.client().get('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ======== Ask Question =============
    def test_delete_question(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        question = Question(content = "test_question", user_id = 25)
        question.setID(100)
        question.insert()
        Asked(user_id = 28, question_id = 100).insert()
    def testFail_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ========= Patch Question ============
    def test_patch_question(self):
        res = self.client().patch('/questions/100', json={
            "answer" : "test_answer",
            "reacts" : 3
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["question"]["answer"], "test_answer")
        self.assertEqual(data["question"]["reacts"], 3)
    def testFail_patch_question(self):
        res = self.client().patch('/questions/1000', json={
            "answer" : "test_answer",
            "reacts" : 3})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # =========== Replys Question ===========
    def test_add_reply(self):
        res = self.client().post('/questions/100/replys', json = {
            "reply" : "test_reply",
            "asker_id" : 28
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

        Question.query.get(data['id']).delete()
        QuestionReplys.query.filter(QuestionReplys.reply_id == data['id']).all()[0].delete()

    def testFail_add_reply(self):
        res = self.client().post('/questions/100/replys', json = {
            "reply" : "test_reply",
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        
    # ============= Get Reply ================
    def test_get_reply(self):
        res = self.client().get('/questions/100/replys')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data["reply"]) , 1)
        self.assertEqual(data["reply"][0]["user_id"], 25)
        self.assertEqual(data["reply"][0]["content"], "test_reply")

    def testFail_get_reply(self):
        res = self.client().get('/questions/1000/replys')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        
    # ============ Get User =======================
    def test_get_user(self):
        res = self.client().get('/users/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['user']["name"], "test_user")
        self.assertEqual(data['user']["id"], 100)
        

    def testFail_get_user(self):
        res = self.client().get('/users/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Patch User =======================
    def test_patch_user(self):
        res = self.client().patch('/users/100', json = {
            "picture" : "path_to_picture"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['user']["name"], "test_user")
        self.assertEqual(data['user']["picture"], "path_to_picture")
        

    def testFail_patch_user(self):
        res = self.client().patch('/users/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Get Asked Questions ================
    def test_asked_questions(self):
        res = self.client().get('/users/100/asked_questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data['questions']), 0)
        self.assertTrue(data['success'])
        

    def testFail_asked_questions(self):
        res = self.client().get('/users/1000/asked_questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Get User's Questions ================
    def test_users_questions(self):
        res = self.client().get('/users/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data['questions']), 0)
        self.assertTrue(data['success'])
        

    def testFail_users_questions(self):
        res = self.client().get('/users/1000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Ask  Questions ================
    def test_ask_questions(self):
        res = self.client().post('/users/100/questions', json= {
            "id" : 100,
            "question" : "recursive_question"
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['question']['content'], "recursive_question")
        self.assertEqual(data['question']['user_id'], 100)

        id = data['question']["id"]
        question = Question.query.get(id)
        question.delete()

        Asked.query.filter(Asked.question_id == id).all()[0].delete()


    def testFail_ask_question(self):
        res = self.client().post('/users/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Get Followers ================
    def test_get_followers(self):
        res = self.client().get('/users/100/followers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data['followers']), 1)
        self.assertTrue(data['success'])
        
    def testFail_get_followers(self):
        res = self.client().get('/users/1000/followers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Follow User ================
    def test_post_followers(self):
        res = self.client().post('/users/100/followers', json= {
            "id" : 101
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['followed'], 101)
        self.assertTrue(data['success'])
        
    def testFail_post_followers(self):
        res = self.client().post('/users/100/followers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Reports ================
    def test_get_reports(self):
        res = self.client().get('/reports')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        # Admin Fail Case

    def test_add_reports(self):
        res = self.client().post('/reports', json = {
            "user_id" : 101,
            "question_id" : 28
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        Report.query.filter(Report.user_id == 101 and Report.question_id == 28).all()[0].delete()

    def testFail_add_reports(self):
        res = self.client().post('/reports')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Get 1 Report ============
    def test_get_report(self):
        res = self.client().get('/reports/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['report']['id'], 100)
    def testFail_get_report(self):
        res = self.client().get('/reports/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============== Delete Report ===========
    def test_delete_reports(self):
        res = self.client().delete('/reports/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_report'], 100)

        report = Report(user_id = 100, question_id = 100)
        report.setID(100)
        report.insert()

    def testFail_delete_reports(self):
        res = self.client().delete('/reports/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
