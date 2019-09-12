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
    pass