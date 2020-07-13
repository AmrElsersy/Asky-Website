admin_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IloxaGFneUZaSkVySGVMbnpLcHdmQiJ9.eyJpc3MiOiJodHRwczovL3NlcnN5LmF1dGgwLmNvbS8iLCJzdWIiOiJnaXRodWJ8MzU2MTM2NDUiLCJhdWQiOlsiQXNreSIsImh0dHBzOi8vc2Vyc3kuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5NDYwMTE1NiwiZXhwIjoxNTk0Njg3NTU2LCJhenAiOiJ1MHkwaXJwS0RnZTVCSENhZGg3VTduaTlxQjJpaDVkdyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6cXVlc3Rpb24iLCJkZWxldGU6cmVwb3J0IiwiZ2V0OnF1ZXN0aW9uIiwiZ2V0OnJlcG9ydCIsImdldDp1c2VyX2luZm8iXX0.j7e19voWGgC-aF3CqhtSAfGuhC7rD5bM11lipF7Sth2zX5pwKTV7MuPpLQcsD96nyMKqKvBOAS2apazocTvZ-WDEfsV9QPLG9FPFE8epSOlMSoevApq3KDTr9OW0aK7_qf0PkT-F-esb7DOS8KU3q6sR-g9PBBvsIWS5I7sDfRCoZo2YBYbiXC1OFQp5Vc9sZcQ-4sgyjsgCcOJ03oLAZh_MfKTESuxrPchI02CC4gcgu6qoG2rb_BLGziBy7jOZGB__hTdspwMMFoKWVoGnlvkEghMqY96FsKkFW4QBiDouejPtx2A4htRvdWXefqmt8BokrY01rthctFhili4XEw"
user_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IloxaGFneUZaSkVySGVMbnpLcHdmQiJ9.eyJpc3MiOiJodHRwczovL3NlcnN5LmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzkwNDIxOTE1MjAzMzQ0MzQ1MyIsImF1ZCI6WyJBc2t5IiwiaHR0cHM6Ly9zZXJzeS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTk0NjAxNTc5LCJleHAiOjE1OTQ2ODc5NzksImF6cCI6InUweTBpcnBLRGdlNUJIQ2FkaDdVN25pOXFCMmloNWR3Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDpyZXBvcnQiLCJhbnN3ZXI6cXVlc3Rpb24iLCJhc2s6cXVlc3Rpb24iLCJmb2xsb3c6cHJvZmlsZSIsImdldDpxdWVzdGlvbiIsImdldDp1c2VyX2luZm8iXX0.NS-LiBaxyXKu67JiaMhg1BsBdrr5IhfubM42bZ-3KDhT5okHty8mCpxHb75qAq3i6qkzAWkyHjE-KQ3ow0WJ8ItBuzNUJwYkq0w83egje8eTOnbyZsyH8p06oEyX8y_5zl3F3xp-i8E_jjpP7xvhz7cKj1Pm67mAL6BwU43Y9gmXyID0sgNjelb_jN5IpFy5A7sqjE985Jf3XpT-KoAUFHiNABo3WOoPkYkk-Y8uq1JFNu9QGsCsEN4fFnO4iBCa-zCDeKCnwZNb4AD__ICB3ScHg24Ed7gyflIhYHf3091KiUyht7JRMiHGgtVqcNI3udtUosHVB0b9mK7iFWMAoA"
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
        self.admin = {"Authorization" : "Bearer " + admin_token }
        self.user  = {"Authorization" : "Bearer " + user_token }

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # ======= Get Question ============
    def test_get_question(self):
        res = self.client().get('/questions/100', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['question']['content'], "test_question")
        self.assertEqual(data['question']['user_id'], 25)
    def testFail_get_question(self):
        res = self.client().get('/questions/1000', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ======== delete Question =============
    def test_delete_question(self):
        res = self.client().delete('/questions/100', headers = self.admin)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        question = Question(content = "test_question", user_id = 25)
        question.setID(100)
        question.insert()
        Asked(user_id = 28, question_id = 100).insert()
    def testFail_delete_question(self):
        res = self.client().delete('/questions/1000', headers = self.admin)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ========= Patch Question ============
    def test_patch_question(self):
        res = self.client().patch('/questions/100', json={
            "answer" : "test_answer",
            "reacts" : 3
        }, headers = self.user)

        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["question"]["answer"], "test_answer")
        self.assertEqual(data["question"]["reacts"], 3)
    
    def testFail_patch_question(self):
        res = self.client().patch('/questions/1000', json={
            "answer" : "test_answer",
            "reacts" : 3}, headers = self.user)

        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # =========== Replys Question ===========
    def test_add_reply(self):
        res = self.client().post('/questions/100/replys', json = {
            "reply" : "test_reply",
            "asker_id" : 28
        }, headers = self.user)

        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

        Question.query.get(data['id']).delete()
        QuestionReplys.query.filter(QuestionReplys.reply_id == data['id']).all()[0].delete()

    def testFail_add_reply(self):
        res = self.client().post('/questions/100/replys', json = {
            "reply" : "test_reply",
        }, headers = self.user)

        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        
    # ============= Get Reply ================
    def test_get_reply(self):
        res = self.client().get('/questions/100/replys', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data["reply"]) , 1)
        self.assertEqual(data["reply"][0]["user_id"], 25)
        self.assertEqual(data["reply"][0]["content"], "test_reply")

    def testFail_get_reply(self):
        res = self.client().get('/questions/1000/replys', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        
    # ============ Get User =======================
    def test_get_user(self):
        res = self.client().get('/users/100', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['user']["name"], "test_user")
        self.assertEqual(data['user']["id"], 100)
        

    def testFail_get_user(self):
        res = self.client().get('/users/1000', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Patch User =======================
    def test_patch_user(self):
        res = self.client().patch('/users/100', json = {
            "picture" : "path_to_picture"
        } , headers = self.user)

        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['user']["name"], "test_user")
        self.assertEqual(data['user']["picture"], "path_to_picture")
        

    def testFail_patch_user(self):
        res = self.client().patch('/users/1000' , headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Get Asked Questions ================
    def test_asked_questions(self):
        res = self.client().get('/users/100/asked_questions', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data['questions']), 0)
        self.assertTrue(data['success'])
        

    def testFail_asked_questions(self):
        res = self.client().get('/users/1000/asked_questions', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Get User's Questions ================
    def test_users_questions(self):
        res = self.client().get('/users/100/questions', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data['questions']), 0)
        self.assertTrue(data['success'])
        

    def testFail_users_questions(self):
        res = self.client().get('/users/1000/questions', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Ask  Questions ================
    def test_ask_questions(self):
        res = self.client().post('/users/100/questions', json= {
            "id" : 100,
            "question" : "recursive_question"
        }, headers = self.user)

        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['question']['content'], "recursive_question")
        self.assertEqual(data['question']['user_id'], 100)

        id = data['question']["id"]
        question = Question.query.get(id)
        question.delete()

        Asked.query.filter(Asked.question_id == id).all()[0].delete()


    def testFail_ask_question(self):
        res = self.client().post('/users/100/questions', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Get Followers ================
    def test_get_followers(self):
        res = self.client().get('/users/100/followers', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual( len(data['followers']), 1)
        self.assertTrue(data['success'])
        
    def testFail_get_followers(self):
        res = self.client().get('/users/1000/followers', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============ Follow User ================
    def test_post_followers(self):
        res = self.client().post('/users/100/followers', json= {
            "id" : 101
        }, headers = self.user)
        data = json.loads(res.data)
  
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['followed'], 101)
        self.assertTrue(data['success'])
        
    def testFail_post_followers(self):
        res = self.client().post('/users/100/followers', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Reports ================
    def test_get_reports(self):
        res = self.client().get('/reports', headers = self.admin)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        # Admin Fail Case

    def test_add_reports(self):
        res = self.client().post('/reports', json = {
            "user_id" : 101,
            "question_id" : 28
        }, headers = self.user )

        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])

        Report.query.filter(Report.user_id == 101 and Report.question_id == 28).all()[0].delete()

    def testFail_add_reports(self):
        res = self.client().post('/reports', headers = self.user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)

    # ============ Get 1 Report ============
    def test_get_report(self):
        res = self.client().get('/reports/100', headers = self.admin)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['report']['id'], 100)

    def testFail_get_report(self):
        res = self.client().get('/reports/1000', headers = self.admin)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)

    # ============== Delete Report ===========
    def test_delete_reports(self):
        res = self.client().delete('/reports/100', headers = self.admin)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_report'], 100)

        report = Report(user_id = 100, question_id = 100)
        report.setID(100)
        report.insert()

    def testFail_delete_reports(self):
        res = self.client().delete('/reports/1000', headers = self.admin)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
