from django.test import TestCase

from ...utils import PasswordUtils
from ...models import User, UserGroup, Privelege

class UserTest(TestCase):
    def create_user(self, name, email, password, group=None):
        pass_data = PasswordUtils.get_password(password)
        
        user = User.objects.create(
            name=name,
            email=email,
            group=group,
            pass_hash=pass_data['pass_hash'],
            pass_salt=pass_data['pass_salt'],
            pass_algo=pass_data['pass_algo']
        )

        return user

    def update_user(self, id, **kwargs):
        user = User.objects.get(id=id)
        user.name = kwargs.get('name', user.name)
        user.email = kwargs.get('email', user.email)
        user.group = kwargs.get('group', user.group)
        
        password = kwargs.get('password', None)
        if password is not None:
            password = PasswordUtils.get_password(password)
            user.pass_hash = password['pass_hash']
            user.pass_salt = password['pass_salt']
            user.pass_algo = password['pass_algo']
        
        user.save

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