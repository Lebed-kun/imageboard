from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from django.core.files.base import ContentFile
import base64
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

# Helpers

def edit_board_data(request, board):
    board.name = request.data,get('name', board.name)
    board.abbr = request.data.get('abbr', board.abbr)
    board.description = request.data.get('description', board.description)
    board.bump_limit = request.data.get('bump_limit', board.bump_limit)
    board.spam_words = request.data.get('spam_words', board.spam_words)

    remove_picture = request.data.get('remove_picture', False)
    if remove_picture:
        board.picture = None
    picture = request.data.get('picture', None)
    if picture is not None:
        picture = ContentFile(base64.b64decode(picture['content']), name=picture['name'])
        board.picture = picture
            
    board.save()

    data = {
        'name' : board.name,
        'abbr' : board.abbr,
        'description' : board.description,
        'bump_limit' : board.bump_limit,
        'spam_words' : board.spam_words,
        'picture' : board.picture.url if board.picture else None,
        'author' : board.author.name,
        'created_at' : board.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at' : board.updated_at.strftime('%d/%m/%Y %H:%M:%S')
    }

    return data

# Views

@api_view(('PUT',))
@renderer_classes((JSONRenderer,))
def edit_board(request, id, *args, **kwargs):
    if request.method == 'PUT':
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
            data = edit_board_data(request, board)
            return Response(data, status=status.HTTP_202_ACCEPTED, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == board:
                    data = edit_board_data(request, board)
                    return Response(data, status=status.HTTP_202_ACCEPTED, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to edit board /{}/.'.format(board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')