from django.test import TestCase

from ... import models

# Test models for moderating

class ReportTest(TestCase):
    def setUp(self):
        board = models.Board.objects.create(name='General', abbr='b')
        thread = models.Thread.objects.create(board=board)
        post = models.Post.objects.create(
            message='The quick brown fox.', 
            poster_ip='230.78.0.16',
            thread=thread
        )
    
    def create_report(self, reason):
        post = models.Post.objects.get(id=1)
        report = models.Report.objects.create(post=post, reason=reason)
        return report
    
    def test_create_report(self):
        report = self.create_report('Dummy text.')
        self.assertEqual(report.reason, 'Dummy text.')

        print('Report created at: ' + str(report.created_at))

class BanTest(TestCase):
    def setUp(self):
        board = models.Board.objects.create(name='General', abbr='b')
        thread = models.Thread.objects.create(board=board)
        post = models.Post.objects.create(
            message='The quick brown fox.', 
            poster_ip='230.78.0.16',
            thread=thread
        )

    def create_ban(self, poster_ip, reason, expired_at, board=None):
        ban = models.Ban.objects.create(
            poster_ip=poster_ip,
            reason=reason,
            expired_at=expired_at,
            board=board
        )
        return ban

    def update_ban(self, **kwargs):
        ban = models.Ban.objects.get(id=1)
        ban.expired_at = kwargs.get('expired_at', ban.expired_at)
        ban.save()
        return ban
    
    def test_create_ban_local(self):
        poster_ip = models.Post.objects.get(id=1).poster_ip
        reason = 'Dummy text.'
        expired_at = '2019-11-11'
        board = models.Board.objects.get(id=1)

        ban = self.create_ban(poster_ip, reason, expired_at, board)
        self.assertEqual(ban.poster_ip, poster_ip)
        self.assertEqual(ban.reason, reason)
        self.assertEqual(ban.expired_at, expired_at)
        self.assertEqual(ban.board, board)

    def test_create_ban_global(self):
        poster_ip = models.Post.objects.get(id=1).poster_ip
        reason = 'Dummy text.'
        expired_at = '2019-11-11'

        ban = self.create_ban(poster_ip, reason, expired_at)
        self.assertEqual(ban.poster_ip, poster_ip)
        self.assertEqual(ban.reason, reason)
        self.assertEqual(ban.expired_at, expired_at)
        self.assertEqual(ban.board, None)

    def test_update_ban(self):
        poster_ip = models.Post.objects.get(id=1).poster_ip
        reason = 'Dummy text.'
        expired_at = '2019-11-11'
        board = models.Board.objects.get(id=1)
        self.create_ban(poster_ip, reason, expired_at, board)

        expired_at_new = '2019-09-20'
        ban = self.update_ban(expired_at=expired_at_new)
        self.assertEqual(ban.expired_at, expired_at_new)

        print(ban.created_at)
        print(ban.updated_at)

# Done!