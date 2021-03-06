import random
import base64
import re
from hashlib import sha1, md5, sha256
from django.db.models import Q

class StringUtils:
    @staticmethod
    def concat(str1, str2):
        return str1 + str2
    
    @staticmethod
    def merge(str1, str2):
        result = ''

        i, j = 0, 0
        while i < len(str1) or j < len(str2):
            if i < len(str1) and j < len(str2):
                result += str1[i] + str2[j]
                i += 1
                j += 1
            elif i < len(str1):
                result += str1[i]
                i += 1
            else:
                result += str2[j]
                j += 1
        
        return result

    @staticmethod
    def reverse(str1):
        result = ''

        i = len(str1) - 1
        while i >= 0:
            result += str1[i]
            i -= 1
        
        return result

    @staticmethod
    def random(length=100):
        MIN_CHARACTER = ord('!')
        MAX_CHARACTER = ord('~')

        result = ''

        for _ in range(length):
            char = random.randint(MIN_CHARACTER, MAX_CHARACTER)
            result += chr(char)
        
        return result

class PasswordUtils:
    STRING_ALGORITHMS = {
        'concat' : (lambda str1, str2 : StringUtils.concat(str1, str2)),
        'merge' : (lambda str1, str2 : StringUtils.merge(str1, str2)),
        'concat_reverse' : (lambda str1, str2 : StringUtils.concat(StringUtils.reverse(str1), str2)),
        'merge_reverse' : (lambda str1, str2 : StringUtils.merge(StringUtils.reverse(str1), str2))
    }

    @staticmethod
    def get_hash_pass(algorithm_crypt, algorithm_string, raw_password, salt):
        scrambled_password = PasswordUtils.STRING_ALGORITHMS[algorithm_string](raw_password, salt)
        scrambled_password = scrambled_password.encode('utf-8')

        if algorithm_crypt == 'sha1':
            return sha1(scrambled_password).hexdigest()
        elif algorithm_crypt == 'sha256':
            return sha256(scrambled_password).hexdigest()
        elif algorithm_crypt == 'md5':
            return md5(scrambled_password).hexdigest()
        raise ValueError("Got unknown password algorithm type in password.")

    @staticmethod
    def get_password(raw_password):
        algorithm_crypt = random.choice(['sha1', 'sha256', 'md5'])
        algorithm_string = random.choice(['concat', 'merge', 'concat_reverse', 'merge_reverse'])
        salt = StringUtils.random()
        password = PasswordUtils.get_hash_pass(algorithm_crypt, algorithm_string, raw_password, salt)

        pass_data = {
            'pass_hash' : password,
            'pass_salt' : salt,
            'pass_algo' : algorithm_crypt + '+' + algorithm_string
        }

        return pass_data

def get_visitor_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')

def full_text_found(fields, query):
    words = query.split('+')
    condition = Q()
    
    for word in words:
        for field in fields:
            full_field = field + '__icontains'
            condition |= Q(**{
                full_field  : word
            })

    return condition

def base64decode(data):
    data = data.split(';base64,')
    data = data[-1]
    
    return base64.b64decode(data)
