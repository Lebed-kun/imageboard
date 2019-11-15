from rest_framework.response import Response
from django.core.files.base import ContentFile
from rest_framework import status
from datetime import datetime, timezone
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

@api_view(('DELETE',))
@renderer_classes((JSONRenderer,))
def delete_board(request, id, *args, **kwargs):
    if request.method == 'DELETE':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if user has access to delete boards
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.DELETE_BOARDS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to delete boards.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if board exists
        board = None
        try:
            board = models.Board.objects.get(id=id)
        except models.Board.DoesNotExist:
            message = {
                'message' : 'Board doesn\'t exist.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        # Success
        if user_priveleges[0]['board'] is None:
            board.delete()
            message = {
                'message' : 'Delete succeed.'
            }
            return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == board:
                    board.delete()
                    message = {
                        'message' : 'Delete succeed.'
                    }
                    return Response(message, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to delete board /{}/.'.format(board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('DELETE',))
@renderer_classes((JSONRenderer,))
def remove_priv_user(request, abbr, group_name, id, *args, **kwargs):
    if request.method == 'DELETE':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if user has access to edit boards
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.EDIT_BOARDS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to edit boards.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if board exists
        board = models.Board.objects.filter(abbr=abbr)
        if len(board) == 0:
            message = {
                'message' : 'Board /{}/ doesn\'t exists.'.format(abbr)
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        board = board[0]

        # Check if user to be unpriveleged exists
        priv_user = None
        try:
            priv_user = models.User.objects.get(id=id)
        except models.User.DoesNotExist:
            message = {
                'message' : 'User doesn\'t exists.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        # Success
        group = models.UserGroup.objects.filter(Q(name__icontains=group_name) & Q(board=board))[0]
        if user_priveleges[0]['board'] is None:
            priv_user.groups.remove(group)
            priv_user.save()

            message = {
                'message' : 'User {} is removed from {}s successfully!'.format(username, group_name.lower())
            }
            return Response(message, status=status.HTTP_202_ACCEPTED, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == board:
                    priv_user.groups.remove(group)
                    priv_user.save()

                    message = {
                        'message' : 'User {} is removed from {}s successfully!'.format(username, group_name.lower())
                    }
                    return Response(message, status=status.HTTP_202_ACCEPTED, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to edit board /{}/.'.format(board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')