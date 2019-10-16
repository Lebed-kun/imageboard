from .... import models
from ....utils import StringUtils, PasswordUtils
from .... import priveleges

class TestHelpers:
    @staticmethod
    def create_board(name, abbr):
        board = models.Board.objects.create(**{
            'name' : board_name,
            'abbr' : board_abbr
        })
        return board

    @staticmethod
    def create_token(expired_at, ip):
        data = {
            'value' : StringUtils.random(),
            'expired_at' : expired_at,
            'ip' : ip
        }

        token = models.UserToken.objects.create(**data)

        return token

    @staticmethod
    def create_user(name, email, password):
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

    @staticmethod
    def create_privelege():
        moder_privelege = models.Privelege.objects.create(**{
            'name' : priveleges.GET_REPORTS,
            'description' : 'Get last reports of boards'
        })

        return moder_privelege 

    @staticmethod
    def create_moder(name, privelege, board_abbr=None):
        board = None
        if board_abbr:
            board = models.Board.objects.filter(abbr=board_abbr)[0]
        
        moder_group = models.UserGroup.objects.create(**{
            'name' : name,
            'board' : board
        })
        moder_group.priveleges.add(privelege)
        moder_group.save()

        return moder_group