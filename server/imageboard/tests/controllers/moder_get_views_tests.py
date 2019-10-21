from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.moder import get_views
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
        post_bb1 = models.Post.objects.create(**{
            'message' : 'Hello world.',
            'poster_ip' : '100.200.101.103',
            'thread' : thread_bb
        })
        post_bb2 = models.Post.objects.create(**{
            'message' : 'Fuck you bitch!',
            'poster_ip' : '88.204.128.110',
            'thread' : thread_bb
        })
        report_bb2 = models.Report.objects.create(**{
            'post' : post_bb2,
            'board' : board_bb,
            'reason' : 'Offensive words'
        })
        post_bb3 = models.Post.objects.create(**{
            'message' : 'dshfdsyvfds vfsdufgdsvbfds f',
            'poster_ip' : '108.16.190.72',
            'thread' : thread_bb
        })
        report_bb3 = models.Report.objects.create(**{
            'post' : post_bb3,
            'board' : board_bb,
            'reason' : 'Gibberish'
        })

    def setUp_reports_c(self):
        board_c = models.Board.objects.create(**{
            'name' : 'Creative',
            'abbr' : 'c'
        })
        thread_c = models.Thread.objects.create(board=board_c)
        post_c1 = models.Post.objects.create(**{
            'message' : 'Hello world.',
            'poster_ip' : '100.200.101.103',
            'thread' : thread_c
        })
        post_c2 = models.Post.objects.create(**{
            'message' : 'Fuck you bitch!',
            'poster_ip' : '88.204.128.110',
            'thread' : thread_c
        })
        report_с2 = models.Report.objects.create(**{
            'post' : post_c2,
            'board' : board_c,
            'reason' : 'Offensive'
        })
        post_c3 = models.Post.objects.create(**{
            'message' : 'dshfdsyvfds vfsdufgdsvbfds f',
            'poster_ip' : '108.16.190.72',
            'thread' : thread_c
        })
        report_c3 = models.Report.objects.create(**{
            'post' : post_c3,
            'board' : board_c,
            'reason' : 'Flood'
        })

    def setUp_users(self):
        moder_privelege = TestHelpers.create_privelege(priveleges.GET_REPORTS)
        
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
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_last_reports(request, ip='200.48.100.81')

        self.assertEqual(response.data['message'], 'User is not authorized.')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, 'application/json')

    # Done!
    def test_user_restricted(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_last_reports(request, ip='200.200.100.10')

        self.assertEqual(response.data['message'], 'User doesn\'t have permission to view reports.')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, 'application/json')

    # Done!
    def test_success_local(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_last_reports(request, ip='123.40.80.101')

        self.assertEqual(response.data['pages_count'], 1)
        self.assertEqual(response.data['prev_page'], None)
        self.assertEqual(response.data['next_page'], None)
        self.assertEqual(len(response.data['results']), 2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        print(response.data)

    # Done!
    def test_success_global(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_last_reports(request, ip='103.48.88.101')

        self.assertEqual(response.data['pages_count'], 1)
        self.assertEqual(response.data['prev_page'], None)
        self.assertEqual(response.data['next_page'], None)
        self.assertEqual(len(response.data['results']), 4)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        print(response.data)

class GetLastBansTest(TestCase):
    def setUp_bans(self):
        board_mu = models.Board.objects.create(**{
            'name' : 'Music',
            'abbr' : 'mu'
        })
        board_ya = models.Board.objects.create(**{
            'name' : 'Yaoi',
            'abbr' : 'ya'
        })

        ban_mu = models.Ban.objects.create(**{
            'board' : board_mu,
            'poster_ip' : '144.88.100.200',
            'expired_at' : '2024-01-01',
            'reason' : 'Antiukrainian propaganda'
        })
        ban_ya = models.Ban.objects.create(**{
            'board' : board_ya,
            'poster_ip' : '98.80.191.7',
            'expired_at' : '2024-01-01',
            'reason' : 'Homophobic propaganda'
        })
        ban_global = models.Ban.objects.create(**{
            'poster_ip' : '111.200.140.1',
            'expired_at' : '2024-01-01',
            'reason' : 'Wipe'
        })

    def setUp_users(self):
        moder_privelege = TestHelpers.create_privelege(priveleges.GET_BANS)
        
        # Local moderator
        moder_group = TestHelpers.create_moder('Moderator', moder_privelege, 'mu')
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
        self.setUp_bans()
        self.setUp_users()

    # Done!
    def test_success_global(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_last_bans(request, ip='103.48.88.101')
        results = response.data['results']

        self.assertEqual(len(results), 3)
        print('Global bans: ', response.data)

    # Done!
    def test_success_local(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_last_bans(request, ip='123.40.80.101')
        results = response.data['results']
        
        self.assertEqual(len(results), 1)
        print('Local bans: ', response.data)

    