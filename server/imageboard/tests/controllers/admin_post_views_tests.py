from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.admin import post_views
from ... import models
from ... import priveleges
from ...utils import StringUtils, PasswordUtils

from .helpers.helpers import TestHelpers

# Done!
class CreateBoardTest(TestCase):
    def setUp(self):
        user = TestHelpers.create_user('JohnByte', 'test111@email.com', '12345678')
        user.token = TestHelpers.create_token('2020-01-01', '123.40.80.101')
        user.save()

    def test(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'name' : 'My Little Pony',
            'abbr' : 'mlp',
            'description' : 'Board for discussions about MLP cartoons and toys :3',
            'bump_limit' : 300,
            'spam_words' : 'faggot,asshole,motherfucker'
        })

        response = post_views.create_board(request, ip='123.40.80.101')

        self.assertEqual(response.data['name'], 'My Little Pony')
        self.assertEqual(response.data['abbr'], 'mlp')
        self.assertEqual(response.data['description'], 'Board for discussions about MLP cartoons and toys :3')
        self.assertEqual(response.data['bump_limit'], 300)
        self.assertEqual(response.data['spam_words'], 'faggot,asshole,motherfucker')
        self.assertEqual(response.data['author'], 'JohnByte')

        print('Created board:', response.data)