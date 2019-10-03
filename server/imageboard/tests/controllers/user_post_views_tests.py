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
    