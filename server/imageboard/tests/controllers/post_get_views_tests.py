from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.post import get_views
from ... import models
from ...utils import PasswordUtils

class GetGeneralBoardTest(TestCase):
    def setUp(self):
        board1 = {
            'name' : 'General',
            'abbr' : 'b'
        }

        board2 = {
            'name' : 'Anime',
            'abbr' : 'a'
        }

        board3 = {
            'name' : 'Programming',
            'abbr' : 'pr'
        }

        board4 = {
            'name' : 'Education',
            'abbr' : 'edu'
        }

        models.Board.objects.create(**board1)
        models.Board.objects.create(**board2)
        models.Board.objects.create(**board3)
        models.Board.objects.create(**board4)

    # Done!
    def test_success(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_general_boards(request)
        
        self.assertEqual(response.data[0], {
            'name' : 'General',
            'abbr' : 'b'
        })
        self.assertEqual(response.data[1], {
            'name' : 'Anime',
            'abbr' : 'a'
        })
        self.assertEqual(response.data[2], {
            'name' : 'Programming',
            'abbr' : 'pr'
        })
        self.assertEqual(response.data[3], {
            'name' : 'Education',
            'abbr' : 'edu'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    # Done!
    def test_bad_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)

        response = get_views.get_general_boards(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')

class GetLastUpdatedThreads(TestCase):
    def setUp(self):
        board = models.Board.objects.create(name='General', abbr='b')

        threads = [
            {
                'board' : board
            },
            {
                'board' : board
            },
            {
                'board' : board
            },
            {
                'board' : board
            }
        ]

        threads_fk = []
        for thread in threads:
            thread_fk = models.Thread.objects.create(**thread)
            threads_fk.append(thread_fk)

        posts = [
            {
                'thread' : threads_fk[0],
                'author' : 'JohnByte',
                'message' : 'Special message',
                'poster_ip' : '67.89.89.128'
            },
            
            {
                'thread' : threads_fk[1],
                'message' : 'Hello world',
                'poster_ip' : '66.66.66.66'
            },

            {
                'thread' : threads_fk[2],
                'message' : 'PINGAS',
                'poster_ip' : '78.88.88.16'
            },
            {
                'thread' : threads_fk[2],
                'message' : 'PINGAS111',
                'poster_ip' : '11.83.88.16'
            },
            
            {
                'thread' : threads_fk[3],
                'author' : 'JohnByte',
                'message' : 'The quick brown fox.S',
                'poster_ip' : '233.80.80.1'
            },
            {
                'thread' : threads_fk[3],
                'message' : 'The quick brown fox.111',
                'poster_ip' : '180.90.83.21'
            },
            {
                'thread' : threads_fk[3],
                'message' : 'The quick brown fox.333',
                'poster_ip' : '133.33.6.66',
                'options' : 'sage'
            } 
        ]

        for post in posts:
            models.Post.objects.create(**post)

    # Done!
    def test_success(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        options = {
            'per_page' : 1,
            'posts_count' : 1
        }
        response = get_views.get_last_updated_threads(request, 'b', **options)

        self.assertEqual(response.data['pages_count'], 4)
        self.assertEqual(response.data['prev_page'], None)
        self.assertEqual(response.data['next_page'], 2)
        
        results = [
            {
                'sticked' : False,
                'read_only' : False,
                'first_post' : {
                    'title' : 'The quick brown fox.S',
                    'author' : 'JohnByte',
                    'contact' : '',
                    'options' : '',
                    'message' : 'The quick brown fox.S'
                },
                'last_posts' : [
                    {
                        'title' : '',
                        'author' : '',
                        'contact' : '',
                        'options' : 'sage',
                        'message' : 'The quick brown fox.333'
                    },
                    {
                        'title' : '',
                        'author' : '',
                        'contact' : '',
                        'options' : '',
                        'message' : 'The quick brown fox.111'
                    }
                ]
            }
        ]
        
        self.assertEqual(response.data['results'][0]['sticked'], False)
        self.assertEqual(response.data['results'][0]['read_only'], False)
        
        print(response.data['results'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    # Done!
    def test_success_search(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)
        request.query_params.update({
            'query' : 'world'
        })

        options = {
            'per_page' : 2,
            'posts_count' : 1
        }
        response = get_views.get_last_updated_threads(request, 'b', **options)

        results = response.data['results'][0]
        self.assertEqual(results['first_post']['title'], 'Hello world')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        print('Queried threads:')
        print(response.data['results'])

    # Done!
    def test_board_not_found(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_last_updated_threads(request, 'pr')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'message' : 'Board not found.'})
        self.assertEqual(response.content_type, 'application/json')

    # Done!
    def test_bad_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)

        response = get_views.get_general_boards(request, 'b')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')

class GetPostsListTest(TestCase):
    def setUp(self):
        board = models.Board.objects.create(name='Anime', abbr='a')
        thread = models.Thread.objects.create(board=board)

        posts = self.get_posts_data(thread)

        for post in posts:
            models.Post.objects.create(**post)

    # Done!
    def get_posts_data(self, thread):
        posts = [
            {
                'message' : 'Hello world',
                'poster_ip' : '100.11.90.79',
                'thread' : thread
            },
            {
                'title' : 'Huita',
                'message' : 'sage sage sage',
                'options' : 'sage',
                'poster_ip' : '34.80.120.111',
                'thread' : thread
            },
            {
                'author' : 'GeneralEmo',
                'contact' : 'http://example.com',
                'message' : ';3',
                'thread' : thread,
                'poster_ip' : '234.90.234.11'
            }
        ]

        return posts
    
    # Done!
    def test_success(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_posts_list(request, 'a', 1)

        print(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    # Done!
    def test_thread_not_found(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_posts_list(request, 'a', 42)

        self.assertEqual(response.data, {'message' : 'Thread not found.'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, 'application/json')

    # Done!
    def test_bad_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request = Request(request)

        response = get_views.get_posts_list(request, 'a', 1)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, 'application/json')

class GetUserBoardsTest(TestCase):
    def setUp(self):
        password = PasswordUtils.get_password('123456')
        
        user1 = models.User.objects.create(**{
            'name' : 'JohnByte',
            'email' : 'test@example.com',
            'pass_hash' : password['pass_hash'],
            'pass_salt' : password['pass_salt'],
            'pass_algo' : password['pass_algo']
        })

        user2 = models.User.objects.create(**{
            'name' : 'Chihiro',
            'email' : 'chihiro@example.com',
            'pass_hash' : password['pass_hash'],
            'pass_salt' : password['pass_salt'],
            'pass_algo' : password['pass_algo']
        })

        board1 = models.Board.objects.create(**{
            'name' : 'Golang',
            'abbr' : 'go',
            'author' : user1
        })

        time.sleep(1)

        board2 = models.Board.objects.create(**{
            'name' : 'Computer science',
            'abbr' : 'cs',
            'author' : user2
        })

        time.sleep(1)

        board3 = models.Board.objects.create(**{
            'name' : 'Bondage',
            'abbr' : 'bndg',
            'author' : user1
        })

    # Done!
    def test_success(self):
        request = HttpRequest()
        request.method = 'GET'
        request = Request(request)

        response = get_views.get_user_boards(request, per_page=2)

        self.assertEqual(response.data['pages_count'], 2)
        self.assertEqual(response.data['prev_page'], None)
        self.assertEqual(response.data['next_page'], 2)
        self.assertEqual(len(response.data['results']), 2)

        print(response.data)