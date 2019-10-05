from django.test import TestCase
from django.http import HttpRequest, QueryDict
from rest_framework.request import Request
from datetime import datetime, timedelta

from ...controllers.user import post_views
from ... import models
from ...utils import PasswordUtils, StringUtils

class IsUserAuthorizedTest(TestCase):
    def setUp(self):
        user1 = self.create_user('John', 'john@example.com', '123456')
        user1.token = self.create_token(datetime(2020, 12, 1), '123.100.200.100')
        user1.save()

        user2 = self.create_user('John666', 'john666@example.com', 'qwertyuiop')
        
        user3 = self.create_user('John111', 'john111@example.com', 'asdfgh1234')
        user3.token = self.create_token(datetime(2018, 1, 1), '100.200.10.11')
        user3.save()

    def create_token(self, expired_at, ip):
        data = {
            'value' : StringUtils.random(),
            'expired_at' : expired_at + timedelta(days=1),
            'ip' : ip
        }

        token = models.UserToken.objects.create(**data)

        return token

    def create_user(self, name, email, password):
        pass_data = PasswordUtils.get_password(password)
        data = {
            'name' : name,
            'email' : email,
            'pass_hash' : pass_data['pass_hash'],
            'pass_salt' : pass_data['pass_salt'],
            'pass_algo' : pass_data['pass_algo']
        }

        user = models.User.objects.create(**data)

        return user

    # Done! 
    def test_valid_token(self):
        is_authorized = post_views.is_user_authorized('123.100.200.100')
        self.assertEqual(is_authorized, True)

    # Done!
    def test_no_token(self):
        is_authorized = post_views.is_user_authorized('88.123.100.101')
        self.assertEqual(is_authorized, False)

    # Done!
    def test_expired_token(self):
        is_authorized = post_views.is_user_authorized('100.200.10.11')
        self.assertEqual(is_authorized, False)

class DoesUserExistTest(TestCase):
    def setUp(self):
        user1 = self.create_user('John', 'john@example.com', '12345678')

    def create_user(self, name, email, password):
        pass_data = PasswordUtils.get_password(password)
        data = {
            'name' : name,
            'email' : email,
            'pass_hash' : pass_data['pass_hash'],
            'pass_salt' : pass_data['pass_salt'],
            'pass_algo' : pass_data['pass_algo']
        }

        user = models.User.objects.create(**data)

        return user

    def test(self):
        user1_by_name = models.User.objects.filter(name='John')
        user1_exists_name = post_views.does_user_exist(user1_by_name)
        
        user1_by_email = models.User.objects.filter(email='john@example.com')
        user1_exists_email = post_views.does_user_exist(user1_by_email)
        
        user2 = models.User.objects.filter(name='Emill')
        user2_exists = post_views.does_user_exist(user2)

        self.assertEqual(user1_exists_email, True)
        self.assertEqual(user1_exists_name, True)
        self.assertEqual(user2_exists, False)

class IsPasswordCorrectTest(TestCase):
    def setUp(self):
        user1 = self.create_user('John', 'john@example.com', '12345678')

    def create_user(self, name, email, password):
        pass_data = PasswordUtils.get_password(password)
        data = {
            'name' : name,
            'email' : email,
            'pass_hash' : pass_data['pass_hash'],
            'pass_salt' : pass_data['pass_salt'],
            'pass_algo' : pass_data['pass_algo']
        }

        user = models.User.objects.create(**data)

        return user

    def test_success(self):
        user = models.User.objects.filter(name='John')[0]
        correct = post_views.is_password_correct(user, '12345678')
        self.assertEqual(correct, True)

    def test_fail(self):
        user = models.User.objects.filter(name='John')[0]
        correct = post_views.is_password_correct(user, '12345679')
        self.assertEqual(correct, False)

class AuthorizeTest(TestCase):
    def create_user(self, name, email, password):
        pass_data = PasswordUtils.get_password(password)
        data = {
            'name' : name,
            'email' : email,
            'pass_hash' : pass_data['pass_hash'],
            'pass_salt' : pass_data['pass_salt'],
            'pass_algo' : pass_data['pass_algo']
        }

        user = models.User.objects.create(**data)

        return user

    def setUp(self):
        user1 = self.create_user('JohnByte', 'jb@test.net', '12345678')
        user2 = self.create_user('JohnByte1', 'jb111@test.net', '12345678')
        user3 = self.create_user('FelixArgyle', 'felix_argyle@example.com', 'qwertyuiop')

    def test_success_name(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'username' : 'JohnByte',
            'password' : '12345678'
        })

        response = post_views.authorize(request, ip='100.200.18.90')

        self.assertEqual('token' in response.data, True)
        self.assertEqual('expired_at' in response.data, True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        print(response)

    def test_success_email(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'username' : 'jb@test.net',
            'password' : '12345678'
        })

        response = post_views.authorize(request, ip='100.200.18.90')

        self.assertEqual('token' in response.data, True)
        self.assertEqual('expired_at' in response.data, True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        print(response)

    def test_already_authorized(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'username' : 'JohnByte1',
            'password' : '12345678'
        })

        response = post_views.authorize(request, ip='128.200.18.90')
        response = post_views.authorize(request, ip='128.200.18.90')

        self.assertEqual(response.data['message'], 'User already authorized.')

        self.assertEqual(response.status_code, 304)
        self.assertEqual(response.content_type, 'application/json')

    def test_not_exists(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'username' : 'EmeraldGreene',
            'password' : '12345678'
        })

        response = post_views.authorize(request, ip='169.222.18.90')

        self.assertEqual(response.data['message'], 'This user doesn\'t exist.')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, 'application/json')

    def test_incorrect_password(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'username' : 'FelixArgyle',
            'password' : '12345678'
        })

        response = post_views.authorize(request, ip='200.222.32.90')

        self.assertEqual(response.data['message'], 'Incorrect password.')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, 'application/json')