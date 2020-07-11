from app import app
from flask import json
import unittest


class TestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires user login

    def test_correct_login(self):
        tester = app.test_client(self)

        response = tester.post('/home',
                               data=json.dumps({"username": "pjanas", "password": "asdqwe123"}), content_type='application/json', follow_redirects=True)
        print(response.data.decode("utf-8"))
        decoded_response = json.loads(response.data.decode("utf-8"))
        res = 'ok' == decoded_response.get('status')
        print(res)
        self.assertTrue(res)

    def test_wrong_login(self):
        tester = app.test_client(self)

        response = tester.post('/home',
                               data=json.dumps({"username": "wronguser", "password": "wrongpassword"}), content_type='application/json', follow_redirects=True)
        print(response.data.decode("utf-8"))
        decoded_response = json.loads(response.data.decode("utf-8"))
        res = 'nok' == decoded_response.get('status')
        print(res)
        self.assertTrue(res)

    # # Ensure that welcome page loads
    # def test_welcome_route_works_as_expected(self):
    #     response = self.client.get('/welcome', follow_redirects=True)
    #     self.assertIn(b'Welcome to Flask!', response.data)
    #


if __name__ == '__main__':
    unittest.main()
