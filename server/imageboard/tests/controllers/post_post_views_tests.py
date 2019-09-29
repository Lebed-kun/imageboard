from django.test import TestCase
from django.http import HttpRequest, QueryDict
from rest_framework.request import Request
import base64

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

        ban = models.Ban.objects.create(**{
            'poster_ip' : '130.56.80.78',
            'expired_at' : '2020-01-01',
            'reason' : 'Hello world'
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

        files = []
        abs_path = "D:\\Docs\\projects\\imageboard\\server\\imageboard\\tests\\controllers\\files\\"
        with open(abs_path + 'test1.jpg', mode="rb") as file1:
            content = base64.b64encode(file1.read())
            files.append({
                'name' : 'test1.jpg',
                'content' : content
            })
        with open(abs_path + 'test2.png', mode="rb") as file2:
            content = base64.b64encode(file2.read())
            files.append({
                'name' : 'test2.png',
                'content' : content
            })
        request.data.update({
            'files' : files
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

    def test_fail(self):
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

        response = post_views.create_post(request, 'b', 1, poster_ip='130.56.80.78')

        self.assertEqual(response.data['banned'], True)
        self.assertEqual(response.data['board'], '*')
        self.assertEqual(response.data['reason'], 'Hello world')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content_type, 'application/json')

        print(response.data)

class ReportPostsTest(TestCase):
    def setUp(self):
        board = models.Board.objects.create(name='General', abbr='b')
        thread = models.Thread.objects.create(board=board)
        
        post1 = models.Post.objects.create(**{
            'thread' : thread,
            'message' : 'The quick brown fox.',
            'poster_ip' : '107.110.89.10'
        })

        post2 = models.Post.objects.create(**{
            'thread' : thread,
            'message' : 'The quick brown fox.666',
            'poster_ip' : '110.60.11.56'
        })

        post3 = models.Post.objects.create(**{
            'thread' : thread,
            'message' : 'The quick brown fox.333',
            'poster_ip' : '110.60.11.56'
        })

    def test_success(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'reason' : 'Gibberish.'
        })
        ids = [2, 3]

        response = post_views.report_posts(request, 'b', 1, ids)

        self.assertEqual(response.data['message'], 'Report succeed.')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')

        print(response.data)

    def test_fail(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)
        request.data.update({
            'reason' : 'Gibberish.'
        })
        ids = [6]

        response = post_views.report_posts(request, 'b', 1, ids)

        self.assertEqual(response.data['message'], 'Post not found.')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, 'application/json')

        print(response.data)

