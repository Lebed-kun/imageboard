from django.test import TestCase
from django.http import HttpRequest
from rest_framework.request import Request
import time

from ...controllers.post import get_views
from ... import models
from ...utils import PasswordUtils
from ... import priveleges

class GetLastReportsTest(TestCase):
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

    def create_moder(self, name, board_name=None, board_abbr=None):
        moder_privelege = self.create_privelege()
        
        board = None
        if board_name and board_abbr:
            board = models.Board.objects.create(**{
                'name' : board_name,
                'abbr' : board_abbr
            })
        
        moder_group = models.UserGroup.objects.create(**{
            'name' : name,
            'board' : board
        })
        moder_group.priveleges.add(moder_privelege)
        moder_group.save()

        return moder_group
    
    def setUp(self):
        # Local moderator
        moder_group = self.create_moder('Moderator', 'Extra b', 'bb')
        moder = self.create_user('ChiModer', 'test@example.com', '12345678')
        token = self.create_token('2020-01-01', '123.40.80.101')
        moder.groups.add(moder_group)
        moder.token = token
        moder.save()

        # Global moderator
        super_moder_group = self.create_moder('Super moderator')
        super_moder = self.create_user('SuperModer', 'test111@examplee.com', 'qwertyuiop')
        token = self.create_token('2020-01-01', '123.40.80.101')
        super_moder.groups.add(super_moder_group)
        super_moder.token = token
        super_moder.save()

