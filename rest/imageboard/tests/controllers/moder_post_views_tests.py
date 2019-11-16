from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.moder import post_views
from ... import models
from ... import priveleges
from ...utils import StringUtils, PasswordUtils

from .helpers.helpers import TestHelpers

class BanPosterTest(TestCase):
    def setUp_post_bb(self):
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

    def setUp_post_c(self):
        board_c = models.Board.objects.create(**{
            'name' : 'Creative',
            'abbr' : 'c'
        })
        thread_c = models.Thread.objects.create(board=board_c)
        
        post_c1 = models.Post.objects.create(**{
            'message' : 'Ukraine is petukhi.',
            'poster_ip' : '128.202.166.134',
            'thread' : thread_c
        })

        post_c2 = models.Post.objects.create(**{
            'message' : 'Liberals should suck',
            'poster_ip' : '11.216.200.13',
            'thread' : thread_c
        })

    def setUp_users(self):
        moder_privelege = TestHelpers.create_privelege(priveleges.BAN_POSTERS)
        
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
        self.setUp_post_bb()
        self.setUp_post_c()
        self.setUp_users()

    # Done!
    def test_success_global(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'poster_ip' : '128.202.166.134',
            'expired_at' : '2021-01-08',
            'reason' : 'Porusha',
            'board' : 'c'
        })

        response = post_views.ban_poster(request, ip='103.48.88.101')

        self.assertEqual(response.data['poster_ip'], '128.202.166.134')
        self.assertEqual(response.data['expired_at'], '2021-01-08')
        self.assertEqual(response.data['reason'], 'Porusha')
        self.assertEqual(response.data['board'], 'c')

        print(response.data)

    # Done!
    def test_success_local(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'poster_ip' : '100.200.101.103',
            'expired_at' : '2021-01-08',
            'reason' : 'Floood',
            'board' : 'bb'
        })

        response = post_views.ban_poster(request, ip='123.40.80.101')

        self.assertEqual(response.data['poster_ip'], '100.200.101.103')
        self.assertEqual(response.data['expired_at'], '2021-01-08')
        self.assertEqual(response.data['reason'], 'Floood')
        self.assertEqual(response.data['board'], 'bb')

        print(response.data)

    # Done!
    def test_fail_local(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'poster_ip' : '11.216.200.13',
            'expired_at' : '2021-01-08',
            'reason' : 'Totalitarian propaganda',
            'board' : 'c'
        })

        response = post_views.ban_poster(request, ip='123.40.80.101')

        self.assertEqual(response.data['message'], 'User doesn\'t have permission to ban users from board /c/.')

        print(response.data)