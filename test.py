from app import app
from flask import json
from app import User
import unittest


class TestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_correct_login(self):
        tester = app.test_client(self)

        response = tester.post('/home',
                               data=json.dumps({"username": "pjanas", "password": "asdqwe123"}), content_type='application/json', follow_redirects=True)
        decoded_response = json.loads(response.data.decode("utf-8"))
        token = decoded_response.get('token')
        if User.query.filter_by(username='pjanas').first().token == token:
            check = True
        else:
            check = False
        self.assertTrue(check)

    def test_wrong_login(self):
        tester = app.test_client(self)

        response = tester.post('/home',
                               data=json.dumps({"username": "wronguser", "password": "wrongpassword"}),
                               content_type='application/json', follow_redirects=True)
        decoded_response = json.loads(response.data.decode("utf-8"))
        check = 'nok' == decoded_response.get('status')
        self.assertTrue(check)

    def test_session_wrong_token(self):
        tester = app.test_client(self)
        response = tester.post('/history',
                               data=json.dumps({"token": "wrongtoken"}),
                               content_type='application/json', follow_redirects=True)
        decoded_response = json.loads(response.data.decode("utf-8"))
        check = 'wrong token' == decoded_response.get('error')
        self.assertTrue(check)

    def test_session_no_token(self):
        tester = app.test_client(self)
        response = tester.post('/history',
                               data=json.dumps({}),
                               content_type='application/json', follow_redirects=True)
        decoded_response = json.loads(response.data.decode("utf-8"))
        check = 'wrong token' == decoded_response.get('error')
        self.assertTrue(check)

if __name__ == '__main__':
    unittest.main()
