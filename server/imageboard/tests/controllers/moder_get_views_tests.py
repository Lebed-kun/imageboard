from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.post import get_views
from ... import models
from ...utils import PasswordUtils
from ... import priveleges

class GetLastReportsTest(TestCase):
    def create_board(self, name, abbr):
        board = models.Board.objects.create(**{
            'name' : board_name,
            'abbr' : board_abbr
        })
        return board

    def create_token(self, expired_at, ip):
        data = {
            'value' : StringUtils.random(),
            'expired_at' : expired_at,
            'ip' : ip
        }

        token = models.UserToken.objects.create(**data)

        return token

    def create_user(self, name, email, password):
        pass_data = PasswordUtils.get_password(password)
        data = {
            'name' : name,
            'email' : email,
            'pass_hash' : pass_data['pass_hash'],
            'pass_salt' : pass_data['pass_salt'],
            'pass_algo' : pass_data['pass_algo']
        }

        user = models.User.objects.create(**data)

        return user

    def create_privelege(self):
        moder_privelege = models.Privelege.objects.create(**{
            'name' : priveleges.GET_REPORTS,
            'description' : 'Get last reports of boards'
        })

        return moder_privelege 

    def create_moder(self, name, board_abbr=None):
        moder_privelege = self.create_privelege()
        
        board = None
        if board_abbr:
            board = models.Board.objects.filter(abbr=board_abbr)[0]
        
        moder_group = models.UserGroup.objects.create(**{
            'name' : name,
            'board' : board
        })
        moder_group.priveleges.add(moder_privelege)
        moder_group.save()

        return moder_group

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
            'reason' : 'Offensive words'
        })
        post_bb3 = models.Post.objects.create(**{
            'message' : 'dshfdsyvfds vfsdufgdsvbfds f',
            'poster_ip' : '108.16.190.72',
            'thread' : thread_bb
        })
        report_bb3 = models.Report.objects.create(**{
            'post' : post_bb3,
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
            'reason' : 'Offensive'
        })
        post_c3 = models.Post.objects.create(**{
            'message' : 'dshfdsyvfds vfsdufgdsvbfds f',
            'poster_ip' : '108.16.190.72',
            'thread' : thread_c
        })
        report_c3 = models.Report.objects.create(**{
            'post' : post_c3,
            'reason' : 'Flood'
        })

    def setUp_users(self):
        # Local moderator
        moder_group = self.create_moder('Moderator', 'bb')
        moder = self.create_user('ChiModer', 'test@example.com', '12345678')
        token = self.create_token('2020-01-01', '123.40.80.101')
        moder.groups.add(moder_group)
        moder.token = token
        moder.save()

        # Global moderator
        super_moder_group = self.create_moder('Super moderator')
        super_moder = self.create_user('SuperModer', 'test111@examplee.com', 'qwertyuiop')
        token = self.create_token('2020-01-01', '103.48.88.101')
        super_moder.groups.add(super_moder_group)
        super_moder.token = token
        super_moder.save()

        # Moderator (unauthorized)
        moder_ua = self.create_user('Moder007', 'test007@gmail.com', 'asdfghj')
        moder_ua.groups.add(moder_group)
        moder_ua.save()

        # User (authorized)
        user = self.create_user('JohnByte', 'jb1221@mail.com', 'qwertyuiop')
        user.token = self.create_token('2020-01-01', '200.200.100.10')
        user.save()
    
    def setUp(self):
        self.setUp_reports_bb()
        self.setUp_reports_c()
        self.setUp_reports_users()



