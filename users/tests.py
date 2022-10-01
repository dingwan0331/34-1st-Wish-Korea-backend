import json
from urllib import request

from django.test import TestCase, Client

from .models import User

# Create your tests here.
class SignUpTest(TestCase):
    def tearDown(self):
        User.objects.all().delete()

    def test_success_case(self):
        client = Client()
        request_body = {
            'username'     : 'ding',
            'password'     : '123123a!',
            'email'        : 'ding123@gmail.com',
            'phone_number' : '010-1234-1234',
            'first_name'   : '정',
            'last_name'    : '코드',
            'address'      : '서울특별시 강남구 대치동',
            'nick_name'    : 'coding'
            }

        response = client.post('/users/signup', request_body, content_type='application/json')

        self.assertEqual(response.json(), {'message' : 'Created'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_success_case_with_null_true(self):
        client = Client()
        request_body = {
            'username'     : 'ding',
            'password'     : '123123a!',
            'email'        : 'ding123@gmail.com',
            'phone_number' : '010-1234-1234',
            'first_name'   : '정',
            'last_name'    : '코드'
            }

        response = client.post('/users/signup', request_body, content_type='application/json')

        self.assertEqual(response.json(), {'message' : 'Created'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['content-type'], 'application/json')