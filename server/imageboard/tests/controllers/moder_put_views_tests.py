from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.moder import put_views
from ... import models
from ... import priveleges
from ...utils import StringUtils, PasswordUtils

from .helpers.helpers import TestHelpers

class EditPostTest(TestCase):
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
            'reason' : 'Not enough info.'
        })

    def setUp_reports_c(self):
        board_c = models.Board.objects.create(**{
            'name' : 'Creative',
            'abbr' : 'c'
        })
        thread_c = models.Thread.objects.create(board=board_c)
        
        post_c1 = models.Post.objects.create(**{
            'message' : 'Ukraine is petukhi.',
            'poster_ip' : '100.200.101.103',
            'thread' : thread_c
        })
        report_с1 = models.Report.objects.create(**{
            'post' : post_c1,
            'board' : board_c,
            'reason' : 'Porusha'
        })

    def setUp_users(self):
        moder_privelege = TestHelpers.create_privelege(priveleges.EDIT_POSTS)
        
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
    
    def setUp(self):
        self.setUp_reports_bb()
        self.setUp_reports_c()
        self.setUp_users()

    def test_success_global(self):
        request = HttpRequest()
        request.method = 'PUT'
        request = Request(request)
        request.data.update({
            'message' : 'Ukraine has gorilka.'
        })

        response = put_views.edit_post(request, 2, ip='103.48.88.101')

        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['message'], 'Ukraine has gorilka.')
        print(response.data)

    def test_success_local(self):
        request = HttpRequest()
        request.method = 'PUT'
        request = Request(request)
        request.data.update({
            'message' : 'Hello world. This is test thread.'
        })

        response = put_views.edit_post(request, 1, ip='123.40.80.101')

        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['message'], 'Hello world. This is test thread.')
        print(response.data)

    def test_fail_local(self):
        request = HttpRequest()
        request.method = 'PUT'
        request = Request(request)
        request.data.update({
            'message' : 'HHHHHHHHHHHHH.'
        })

        response = put_views.edit_post(request, 2, ip='123.40.80.101')

        self.assertEqual(response.data['message'], 'User doesn\'t have permission to edit posts from board /c/.')
        self.assertEqual(response.status_code, 403)