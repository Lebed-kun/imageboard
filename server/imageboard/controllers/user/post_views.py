from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from datetime import datetime, timedelta

from ... import models
from ... import constants
from ...utils import get_visitor_ip, PasswordUtils

# Helpers

def is_user_authorized(ip):
    token = models.UserToken.objects.filter(ip=ip)
    if len(token) == 0:
        return False
    token = token[0]

    user = models.User.objects.filter(token=token)[0]
    return user.is_authorized()

def does_user_exist(name_email):
    user = models.User.objects.filter(Q(name=name_email) | Q(email=name_email))
    if len(user) == 0:
        return False
    else:
        return True

def is_password_correct(name_email, password):
    user = models.User.objects.filter(Q(name=name_email) | Q(email=name_email))[0]
    algo_crypt, algo_string = user.pass_algo.split('+')
    pass_hash = PasswordUtils.get_hash_pass(algo_crypt, algo_string, password, user.pass_salt)
    return pass_hash == user.pass_hash

# Views

def authorize(request, name_email, password, *args, **kwargs):
    pass
