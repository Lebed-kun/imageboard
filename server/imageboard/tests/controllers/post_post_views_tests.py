from django.test import TestCase
from django.http import HttpRequest, QueryDict
from rest_framework.request import Request

from ...controllers.post import post_views
from ... import models

# Done!
class IsVisitorBannedTest(TestCase):
    def setUp(self):
        board_b = models.Board.objects.create(name='General', abbr='b')
        board_mu = models.Board.objects.create(name='Music', abbr='mu')

        local_ban = {
            'poster_ip' : '23.224.100.128',
            'expired_at' : '2020-01-01',
            'reason' : 'dhfhudufg',
            'board' : board_mu
        }
        local_ban = models.Ban.objects.create(**local_ban)

        global_ban = {
            'poster_ip' : '100.1.200.11',
            'expired_at' : '2020-01-01',
            'reason' : 'dhfdshfdsghfbvhg'
        }
        global_ban = models.Ban.objects.create(**global_ban)

    def test_local_banned(self):
        bans_mu = post_views.get_bans('23.224.100.128', 'mu')
        banned_mu = post_views.is_visitor_banned(bans_mu['global'], bans_mu['local'])

        bans_b = post_views.get_bans('23.224.100.128', 'b')
        banned_b = post_views.is_visitor_banned(bans_b['global'], bans_b['local'])

        self.assertEqual(banned_mu, True)
        self.assertEqual(banned_b, False)

    def test_global_banned(self):
        bans_mu = post_views.get_bans('100.1.200.11', 'mu')
        banned_mu = post_views.is_visitor_banned(bans_mu['global'], bans_mu['local'])

        bans_b = post_views.get_bans('100.1.200.11', 'b')
        banned_b = post_views.is_visitor_banned(bans_b['global'], bans_b['local'])

        self.assertEqual(banned_mu, True)
        self.assertEqual(banned_b, True)

class CreatePostTest(TestCase):
    def setUp(self):
        board = models.Board.objects.create(name='General', abbr='b')
        thread = models.Thread.objects.create(board=board)
        first_post = models.Post.objects.create(**{
            'message' : 'Hello world!',
            'poster_ip' : '100.32.66.120',
            'thread' : thread
        })

    def test_success(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'title' : 'Hello',
            'author' : 'admin',
            'contact' : 'test@example.ru',
            'options' : 'bump,important',
            'message' : 'The quick brown fox.'
        })

        response = post_views.create_post(request, 'b', 1, poster_ip='234.51.200.88')

        self.assertEqual(response.data['title'], 'Hello')
        self.assertEqual(response.data['author'], 'admin')
        self.assertEqual(response.data['contact'], 'test@example.ru')
        self.assertEqual(response.data['options'], 'bump,important')
        self.assertEqual(response.data['message'], 'The quick brown fox.')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')

        print(response.data)