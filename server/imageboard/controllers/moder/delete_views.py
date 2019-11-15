from rest_framework.response import Response
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from datetime import datetime, timezone

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

@api_view(('DELETE',))
@renderer_classes((JSONRenderer,))
def delete_report(request, id, *args, **kwargs):
    if request.method == 'DELETE':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        # Check if user has access to delete reports
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.DELETE_REPORTS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to delete reports.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if report exists
        report = None
        try:
            report = models.Report.objects.get(id=id)
        except models.Report.DoesNotExist:
            message = {
                'message' : 'Report doesn\'t exist.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        # Success
        if user_priveleges[0]['board'] is None:
            report.delete()
            message = {
                'message' : 'Delete succeed.'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == report.board:
                    report.delete()
                    message = {
                        'message' : 'Delete succeed.'
                    }
                    return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to delete reports from board /{}/.'.format(report.board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('DELETE',))
@renderer_classes((JSONRenderer,))
def delete_post(request, id, *args, **kwargs):
    if request.method == 'DELETE':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        # Check if user has access to delete posts
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.DELETE_POSTS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to delete posts.'
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
            post.delete()
            message = {
                'message' : 'Delete succeed.'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == post.thread.board:
                    post.delete()
                    message = {
                        'message' : 'Delete succeed.'
                    }
                    return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to delete posts from board /{}/.'.format(post.thread.board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('DELETE',))
@renderer_classes((JSONRenderer,))
def delete_thread(request, id, *args, **kwargs):
    if request.method == 'DELETE':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        # Check if user has access to delete threads
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.DELETE_THREADS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to delete threads.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if thread exists
        thread = None
        try:
            thread = models.Thread.objects.get(id=id)
        except models.Thread.DoesNotExist:
            message = {
                'message' : 'Thread doesn\'t exist.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        # Success
        if user_priveleges[0]['board'] is None:
            thread.delete()
            message = {
                'message' : 'Delete succeed.'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == thread.board:
                    thread.delete()
                    message = {
                        'message' : 'Delete succeed.'
                    }
                    return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to delete threads from board /{}/.'.format(thread.board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('DELETE',))
@renderer_classes((JSONRenderer,))
def delete_ban(request, id, *args, **kwargs):
    if request.method == 'DELETE':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        # Check if user has access to delete posts
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.DELETE_BAN)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to delete bans.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if ban exists
        ban = None
        try:
            ban = models.Ban.objects.get(id=id)
        except models.Ban.DoesNotExist:
            message = {
                'message' : 'Ban doesn\'t exist.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        # Success
        if user_priveleges[0]['board'] is None:
            ban.delete()
            message = {
                'message' : 'Delete succeed.'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == ban.board:
                    ban.delete()
                    message = {
                        'message' : 'Delete succeed.'
                    }
                    return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to delete bans from board /{}/.'.format(ban.board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')