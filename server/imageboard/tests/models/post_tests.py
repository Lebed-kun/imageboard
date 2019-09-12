from django.test import TestCase

from ... import models

# Test public models

class BoardTest(TestCase):
    def create_board(self, name, abbr):
        obj = models.Board.objects.create(
            name=name,
            abbr=abbr
        )

        return obj

    def update_board(self, abbr, **kwargs):
        obj = models.Board.objects.filter(abbr=abbr)[0]    
        obj.description = kwargs.get('description', obj.description)
        obj.bump_limit = kwargs.get('bump_limit', obj.bump_limit)
        obj.spam_words = kwargs.get('spam_words', obj.spam_words)

        obj.save()

        return obj

    def test_create_board(self):
        obj = self.create_board('General', 'b')
        self.assertEqual(obj.name, 'General')
        self.assertEqual(obj.abbr, 'b')

        print('Board created at: ' + str(obj.created_at))

    def test_update_board(self):
        self.create_board('General', 'b')
        
        obj = self.update_board(
            'b',
            description='The quick brown fox.', 
            bump_limit=300,
            spam_words='mlm,business,enlarge'
        )

        self.assertEqual(obj.description, 'The quick brown fox.')
        self.assertEqual(obj.bump_limit, 300)
        self.assertEqual(obj.spam_words, 'mlm,business,enlarge')
        print('Board created at: ' + str(obj.created_at))
        print('Board updated at: ' + str(obj.updated_at))


class ThreadTest(TestCase):
    def create_thread(self):
        board = models.Board.objects.create(name='General', abbr='b')

        obj = models.Thread.objects.create(board=board)

        return obj
    
    def update_thread(self, id, **kwargs):
        obj = models.Thread.objects.get(id=id)

        obj.sticked = kwargs.get('sticked', obj.sticked)
        obj.read_only = kwargs.get('read_only', obj.read_only)
        obj.posts_count = kwargs.get('posts_count', obj.posts_count)

        obj.save()

        return obj

    def test_create_thread(self):
        obj = self.create_thread()
        self.assertEqual(obj.id, 1)

        print('Thread created at: ' + str(obj.created_at))

    def test_update_thread(self):
        self.create_thread()

        obj = self.update_thread(
            1,
            sticked=True,
            read_only=True,
            posts_count=700
        )

        self.assertEqual(obj.sticked, True)
        self.assertEqual(obj.read_only, True)
        self.assertEqual(obj.posts_count, 700)
        self.assertEqual(obj.has_bump_limit(), True)

        print('Thread created at: ' + str(obj.created_at))
        print('Thread updated at: ' + str(obj.updated_at))


class PostTest(TestCase):
    def create_posts(self, message, poster_ip, **kwargs):
        board = models.Board.objects.create(name='General111', abbr='c')
        thread = models.Thread.objects.create(board=board)

        results = []
        count = kwargs.get('count', 1)

        for _ in range(count):
            obj = models.Post.objects.create(
                thread=thread,
                message=message,
                poster_ip=poster_ip,
                title=kwargs.get('title', ''),
                author=kwargs.get('author', ''),
                contact=kwargs.get('contact', ''),
                options=kwargs.get('options', '')
            )
            results.append(obj)

        return results

    def update_post(self, id, message):
        obj = models.Post.objects.get(id=id)

        obj.message = message

        obj.save()

        return obj

    def test_create_post_basic(self):
        message = 'The quick brown fox.'
        poster_ip = '127.0.0.1'
        
        obj = self.create_posts(message, poster_ip)[0]
        self.assertEqual(obj.message, message)
        self.assertEqual(obj.poster_ip, poster_ip)
        self.assertEqual(obj.title, message[:20])
        self.assertEqual(obj.thread.first_post, obj)
        self.assertEqual(obj.thread.bumped, True)

        print('Post created at: ' + str(obj.created_at))

    def test_create_multiple_posts(self):
        message = 'The quick brown fox.'
        poster_ip = '178.10.234.80'

        results = self.create_posts(message, poster_ip, count=2)
        
        self.assertEqual(results[0].thread.first_post, results[0])
        self.assertNotEqual(results[1].thread.first_post, results[1])

    def test_create_post(self):
        message = 'The quick brown fox.'
        poster_ip = '178.10.234.80'
        title = 'Hello'
        author = 'JohnByte'
        contact = 'test@example.com'
        options = 'bump'

        obj = self.create_posts(
            message, 
            poster_ip,
            title=title,
            author=author,
            contact=contact,
            options=options
        )[0]
        self.assertEqual(obj.message, message)
        self.assertEqual(obj.poster_ip, poster_ip)
        self.assertEqual(obj.title, title)
        self.assertEqual(obj.author, author)
        self.assertEqual(obj.contact, contact)
        self.assertEqual(obj.options, options)
        self.assertEqual(obj.thread.first_post, obj)

        print('Post created at: ' + str(obj.created_at))

    def test_create_post_sage(self):
        message = 'The quick brown fox.'
        poster_ip = '127.0.0.1'
        
        obj = self.create_posts(message, poster_ip, options='sage')[0]
        self.assertEqual(obj.thread.bumped, False)

        print('Post created at: ' + str(obj.created_at))

    def test_update_post(self):
        message = 'The quick brown fox.'
        poster_ip = '127.0.0.1'
        self.create_posts(message, poster_ip)

        obj = self.update_post(1, 'Hello world')
        self.assertEqual(obj.message, 'Hello world')

        print('Post created at: ' + str(obj.created_at))
        print('Post updated at: ' + str(obj.updated_at))