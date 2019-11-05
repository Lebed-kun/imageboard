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

# Done!
class AddPrivUserTest(TestCase):
    def setUp_board(self):
        board_y = TestHelpers.create_board('Alternative', 'y')

    def setUp_groups(self):
        moder_privelege = TestHelpers.create_privelege(priveleges.GET_REPORTS)
        moder_group = TestHelpers.create_group('Moder', moder_privelege, 'y')

        admin_privelege = TestHelpers.create_privelege(priveleges.EDIT_BOARDS)
        admin_group = TestHelpers.create_group('Admin', admin_privelege, 'y')

        owner = TestHelpers.create_user('JohnByte', 'jb1111@mail.com', '12345678')
        owner.token = TestHelpers.create_token('2020-01-01', '123.100.111.88')
        owner.groups.add(admin_group)
        owner.save()

    def setUp_users(self):
        moder1 = TestHelpers.create_user('ModerY', 'test@example.com', '1234456789')
        moder1.token = TestHelpers.create_token('2024-01-01', '139.100.11.30')
        moder1.save()

        moder2 = TestHelpers.create_user('ModerXY', 'testxy@example.com', '1234456789')
        moder2.token = TestHelpers.create_token('2024-01-01', '140.101.66.48')
        moder2.save()

        admin = TestHelpers.create_user('AdminXXX', 'testxxx@example.com', '1234456789')
        admin.token = TestHelpers.create_token('2024-01-01', '140.160.110.130')
        admin.save()

    def setUp(self):
        self.setUp_board()
        self.setUp_groups()
        self.setUp_users()

    def test_moders(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'username' : 'ModerY'
        })

        response = post_views.add_priv_user(request, 'y', 'Moder', ip='123.100.111.88')
        self.assertEqual(response.data['message'], 'User ModerY became moder successfully!')

        request.data.update({
            'username' : 'ModerXY'
        })
        response = post_views.add_priv_user(request, 'y', 'Moder', ip='123.100.111.88')
        self.assertEqual(response.data['message'], 'User ModerXY became moder successfully!')

    def test_admin(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'username' : 'AdminXXX'
        })

        response = post_views.add_priv_user(request, 'y', 'Admin', ip='123.100.111.88')
        self.assertEqual(response.data['message'], 'User AdminXXX became admin successfully!')