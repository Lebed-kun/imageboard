import random
from django.test import TestCase

from ...utils import StringUtils, PasswordUtils

class StringUtilsTest(TestCase):
    def test_concat(self):
        str1 = 'abcd'
        str2 = 'efgh'
        result = StringUtils.concat(str1, str2)

        self.assertEqual(result, 'abcdefgh')

    def test_merge(self):
        str1 = 'abcdjkl'
        str2 = 'fghi'
        result = StringUtils.merge(str1, str2)

        self.assertEqual(result, 'afbgchdijkl')
    
    def test_reverse(self):
        str1 = 'abcdefg'
        result = StringUtils.reverse(str1)

        self.assertEqual(result, 'gfedcba')

    def test_random(self):
        result = StringUtils.random()
        self.assertEqual(len(result), 100)
        print(result)

class PasswordUtilsTest(TestCase):
    def test_get_hash_pass(self):
        algorithm_crypt = random.choice(['sha1', 'sha256', 'md5'])
        algorithm_string = random.choice(['concat', 'merge', 'concat_reverse', 'merge_reverse'])
        raw_password = StringUtils.random(10)
        salt = StringUtils.random()

        password = PasswordUtils.get_hash_pass(algorithm_crypt, algorithm_string, raw_password, salt)

        print('Crypt algorithm: ' + algorithm_crypt)
        print('String algorithm: ' + algorithm_string)
        print('Raw pass: ' + raw_password)
        print('Salt: ' + salt)
        print('Password: ' + password + '\n')

    def test_get_password(self):
        raw_password = StringUtils.random(10)
        password_data = PasswordUtils.get_password(raw_password)

        print('Raw password: ' + raw_password)
        print('Password data: ' + str(password_data))

# Done: StringUtils, PasswordUtils

