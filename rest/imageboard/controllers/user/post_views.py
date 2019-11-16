from django.db import IntegrityError
from django.db.models import F
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Q
from rest_framework import status
from datetime import datetime, timedelta, timezone
# from django.core.mail import EmailMultiAlternatives

# from server import config

from ... import models
from ... import constants
from ...utils import get_visitor_ip, PasswordUtils, StringUtils

# Helpers

def is_user_authorized(ip):
    token = models.UserToken.objects.filter(ip=ip)
    if len(token) == 0:
        return False
    token = token[0]

    expired = datetime.now(timezone.utc) >= token.expired_at
    if expired:
        token.delete()

    user = models.User.objects.filter(token=token)
    
    return len(user) > 0 and not expired

def does_user_exist(users):
    return users.count() > 0

def is_password_correct(user, password):
    algo_crypt, algo_string = user.pass_algo.split('+')
    pass_hash = PasswordUtils.get_hash_pass(algo_crypt, algo_string, password, user.pass_salt)
    return pass_hash == user.pass_hash

# Views

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def authorize(request, *args, **kwargs):
    if request.method == 'POST':
        ip = kwargs.get('ip', get_visitor_ip(request))
        if is_user_authorized(ip):
            message = {
                'message' : 'User already authorized.'
            }
            return Response(message, status=status.HTTP_304_NOT_MODIFIED, content_type='application/json')
        
        name_email = request.data.get('username')
        user = models.User.objects.filter(Q(name=name_email) | Q(email=name_email))
        
        if not does_user_exist(user):
            message = {
                'message' : 'This user doesn\'t exist.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        user = user[0]
        password = request.data.get('password')
        if not is_password_correct(user, password):
            message = {
                'message' : 'Incorrect password.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        user_token = models.UserToken.objects.create(**{
            'value' : StringUtils.random(200),
            'expired_at' : datetime.now() + timedelta(days=constants.EXPIRATION_DAYS),
            'ip' : ip
        })
        user = models.User.objects.filter(Q(name=name_email) | Q(email=name_email))[0]
        user.token = user_token
        user.save()

        data = {
            'token' : user.token.value,
            'expired_at' : user.token.expired_at.strftime('%d/%m/%Y %H:%M:%S')
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def deauthorize(request, *args, **kwargs):
    if request.method == 'DELETE':
        # Check if user is not authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Success
        token = models.UserToken.objects.filter(ip=ip)[0]
        token.delete()

        message = {
            'message' : 'Logout success.'
        }

        return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def register(request, *args, **kwargs):
    if request.method == 'POST':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if is_user_authorized(ip):
            message = {
                'message' : 'User is already authorized.'
            }
            return Response(message, status=status.HTTP_304_NOT_MODIFIED, content_type='application/json')

        # Check if passwords match
        password = request.data.get('password')
        password1 = request.data.get('password1')
        if password != password1:
            message = {
                'message' : 'Passwords don\'t match.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if user with those name and email exists
        user = None
        try:
            password_data = PasswordUtils.get_password(password) 
            user = models.User.objects.create(**{
                'name' : request.data.get('name'),
                'email' : request.data.get('email'),
                'pass_hash' : password_data['pass_hash'],
                'pass_salt' : password_data['pass_salt'],
                'pass_algo' : password_data['pass_algo']
            })
        except IntegrityError as e:
            if 'unique constraint' in e.args[0] and 'name' in e.args[0]:
                message = {
                    'message' : 'User with this name already exists.'
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
            elif 'unique constraint' in e.args[0] and 'email' in e.args[0]:
                message = {
                    'message' : 'User with this email already exists.'
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
            else:
                return Response(e.args[0], status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

        return Response(message, status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')