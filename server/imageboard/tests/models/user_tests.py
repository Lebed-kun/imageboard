from django.test import TestCase
from datetime import datetime

from ...utils import PasswordUtils, StringUtils
from ...models import User, UserGroup, Privelege, UserToken

# Done!
class UserTest(TestCase):
    def create_user(self, name, email, password, groups=[]):
        pass_data = PasswordUtils.get_password(password)
        
        user = User.objects.create(
            name=name,
            email=email,
            pass_hash=pass_data['pass_hash'],
            pass_salt=pass_data['pass_salt'],
            pass_algo=pass_data['pass_algo']
        )

        user.groups.set(groups)

        return user

    def update_user(self, id, **kwargs):
        user = User.objects.get(id=id)
        user.name = kwargs.get('name', user.name)
        user.email = kwargs.get('email', user.email)
        
        password = kwargs.get('password', None)
        if password is not None:
            password = PasswordUtils.get_password(password)
            user.pass_hash = password['pass_hash']
            user.pass_salt = password['pass_salt']
            user.pass_algo = password['pass_algo']
        
        user.save()

        return user

    def test_create_user(self):
        name = 'JohnByte'
        email = 'test@example.com'
        password = '123456'

        user = self.create_user(name, email, password)

        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        
        print(user.pass_hash)
        print(user.pass_salt)
        print(user.pass_algo)

    def test_update_user(self):
        name = 'JohnByte'
        email = 'test@example.com'
        password = '123456'

        self.create_user(name, email, password)
        
        name = 'JB1221'
        email = 'aaa@test.io'
        password = 'qwertyuiop'

        user = self.update_user(1, name=name, email=email, password=password)

        self.assertEqual(user.name, name)
        self.assertEqual(user.email, email)
        
        print(user.created_at)
        print(user.updated_at)

# Done!
class UserPrivelegesTest(TestCase):
    def setUp(self):
        password = PasswordUtils.get_password('12345678')
        
        privelege = Privelege.objects.create(**{
            'name' : 'get_reports',
            'description' : 'Get reports on posts.'
        })

        user_group = UserGroup.objects.create(**{
            'name' : 'moder'
        })
        user_group.priveleges.add(privelege)
        user_group.save()

        user = User.objects.create(**{
            'name' : 'JohnByte',
            'email' : 'johnbyte@example.com',
            'pass_hash' : password['pass_hash'],
            'pass_salt' : password['pass_salt'],
            'pass_algo' : password['pass_algo']
        })
        user.groups.add(user_group)
        user.save()

    def test(self):
        user = User.objects.filter(name='JohnByte')[0]
        priveleges = user.get_priveleges('get_reports')

        self.assertEqual(len(priveleges), 1)
        self.assertEqual(priveleges[0]['board'], None)
        self.assertEqual(priveleges[0]['privelege'], 'get_reports')