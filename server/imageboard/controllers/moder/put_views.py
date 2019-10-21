from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

def edit_post(request, id, *args, **kwargs):
    if request.method == 'PUT':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        # Check if user has access to edit posts
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.EDIT_POSTS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to edit posts.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if post exists
        post = None
        try:
            post = models.Post.objects.get(id=id)
        except models.Post.DoesNotExist:
            message = {
                'message' : 'Post doesn\'t exist.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        # Success
        if user_priveleges[0]['board'] is None:
            post.message = request.data.get('message', '')
            post.save()
            data = {
                'id' : post.id,
                'message' : post.message,
                'updated_at' : post.updated_at.strftime('%d/%m/%Y %H:%M:%S')
            }
            return Response(data, status=status.HTTP_202_ACCEPTED, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == post.thread.board:
                    post.message = request.data.get('message', '')
                    post.save()
                    data = {
                        'id' : post.id,
                        'message' : post.message,
                        'updated_at' : post.updated_at.strftime('%d/%m/%Y %H:%M:%S')
                    }
                    return Response(data, status=status.HTTP_202_ACCEPTED, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to edit posts from board /{}/.'.format(post.thread.board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

def edit_ban(request, id, *args, **kwargs):
    if request.method == 'PUT':
        pass
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')