from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.moder import delete_views
from ... import models
from ... import priveleges
from ...utils import StringUtils, PasswordUtils

from .helpers.helpers import TestHelpers

class GetLastReportsTest(TestCase):
    def setUp_reports_bb(self):
        board_bb = models.Board.objects.create(**{
            'name' : 'Extra b',
            'abbr' : 'bb'
        })
        thread_bb = models.Thread.objects.create(board=board_bb)
        post_bb = models.Post.objects.create(**{
            'message' : 'Hello world.',
            'poster_ip' : '100.200.101.103',
            'thread' : thread_bb
        })
        report_bb = models.Report.objects.create(**{
            'post' : post_bb,
            'board' : board_bb,
            'reason' : 'Gibberish'
        })

    def setUp_reports_c(self):
        board_c = models.Board.objects.create(**{
            'name' : 'Creative',
            'abbr' : 'c'
        })
        thread_c = models.Thread.objects.create(board=board_c)
        post_c = models.Post.objects.create(**{
            'message' : 'Floooood.',
            'poster_ip' : '100.200.101.103',
            'thread' : thread_c
        })
        report_с = models.Report.objects.create(**{
            'post' : post_c,
            'board' : board_c,
            'reason' : 'Flood'
        })

    def setUp_users(self):
        moder_privelege = TestHelpers.create_privelege()
        
        # Local moderator
        moder_group = TestHelpers.create_moder('Moderator', moder_privelege, 'bb')
        moder = TestHelpers.create_user('ChiModer', 'test@example.com', '12345678')
        token = TestHelpers.create_token('2020-01-01', '123.40.80.101')
        moder.groups.add(moder_group)
        moder.token = token
        moder.save()

        # Global moderator
        super_moder_group = TestHelpers.create_moder('Super moderator', moder_privelege)
        super_moder = TestHelpers.create_user('SuperModer', 'test111@examplee.com', 'qwertyuiop')
        token = TestHelpers.create_token('2020-01-01', '103.48.88.101')
        super_moder.groups.add(super_moder_group)
        super_moder.token = token
        super_moder.save()

        # Moderator (unauthorized)
        moder_ua = TestHelpers.create_user('Moder007', 'test007@gmail.com', 'asdfghj')
        moder_ua.groups.add(moder_group)
        moder_ua.save()

        # User (authorized)
        user = TestHelpers.create_user('JohnByte', 'jb1221@mail.com', 'qwertyuiop')
        user.token = TestHelpers.create_token('2020-01-01', '200.200.100.10')
        user.save()
    
    def setUp(self):
        self.setUp_reports_bb()
        self.setUp_reports_c()
        self.setUp_users()

    # Done!
    def test_user_not_authorized(self):
        request = HttpRequest()
        request.method = 'DELETE'
        request = Request(request)

        response = delete_views.delete_report(request, 1, ip='200.48.100.81')

        self.assertEqual(response.data['message'], 'User is not authorized.')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, 'application/json')

    def test_user_restricted(self):
        request = HttpRequest()
        request.method = 'DELETE'
        request = Request(request)

        response = delete_views.delete_report(request, 1, ip='200.200.100.10')

        self.assertEqual(response.data['message'], 'User doesn\'t have permission to delete reports.')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, 'application/json')