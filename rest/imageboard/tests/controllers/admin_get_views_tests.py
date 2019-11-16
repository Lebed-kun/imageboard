from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request

from ...controllers.admin import get_views
from ... import models
from ... import priveleges
from ...utils import StringUtils, PasswordUtils

from .helpers.helpers import TestHelpers

# Done!
class GetPrivUsersTest(TestCase):
    def setUp_boards(self):
        board_c = TestHelpers.create_board('Creative', 'c')
    
    def setUp_users(self):
        moder_privelege = TestHelpers.create_privelege(priveleges.GET_REPORTS)
        board_c_moder = TestHelpers.create_group('Moder', moder_privelege, 'c')

        admin_privelege = TestHelpers.create_privelege(priveleges.EDIT_BOARDS)
        board_c_admin = TestHelpers.create_group('Admin', admin_privelege, 'c')

        moder1 = TestHelpers.create_user('CMD1337', 'test@example.com', '12345678')
        moder1.token = TestHelpers.create_token('2020-01-01', '123.49.70.13')
        moder1.groups.add(board_c_moder)
        moder1.save()

        moder2 = TestHelpers.create_user('N2ON2O', 'n2o@example.com', '12345678')
        moder2.token = TestHelpers.create_token('2020-01-01', '128.88.75.20')
        moder2.groups.add(board_c_moder)
        moder2.save()

        admin = TestHelpers.create_user('ZeroMaster', 'smd111@test.com', 'qwertyuiop')
        admin.token = TestHelpers.create_token('2020-01-01', '130.89.100.1')
        admin.groups.add(board_c_admin)
        admin.save()

    def setUp(self):
        self.setUp_boards()
        self.setUp_users()

    def test_moders(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_priv_users(request, 'c', 'Moder', ip='130.89.100.1')

        print('Moders of /c/:', response.data)
        self.assertEqual(len(response.data), 2)

    def test_admins(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_priv_users(request, 'c', 'Admin', ip='130.89.100.1')

        print('Admins of /c/:', response.data)
        self.assertEqual(len(response.data), 1)