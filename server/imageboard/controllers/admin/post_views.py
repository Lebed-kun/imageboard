from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from django.core.files.base import ContentFile
import base64

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

# Helpers
def create_group(group_name, privs, board=None):
    if board is not None:
        group = models.UserGroup.objects.create(**{
            'name' : '{} of /{}/'.format(group_name, board.abbr),
            'board' : board
        })
    else:
        group = models.UserGroup.objects.create(**{
            'name' : group_name
        })
    
    priveleges = models.Privelege.objects.filter(name__in=privs)
    for priv in priveleges:
        group.priveleges.add(priv)
    group.save()

    return group

# Views

def create_board(request, *args, **kwargs):
    if request.method == 'POST':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Create board
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]

        picture = request.data.get('picture', None)
        if picture is not None:
            picture = ContentFile(base64.b64decode(picture['content']), name=picture['name'])

        board = models.Board.objects.create(**{
            'name' : request.data.get('name'),
            'abbr' : request.data.get('abbr'),
            'description' : request.data.get('description', ''),
            'bump_limit' : request.data.get('bump_limit', 500),
            'spam_words' : request.data.get('spam_words', ''),
            'picture' : picture,
            'author' : user
        })

        # Create admin and moder groups of the board
        admin_group = create_group('Admin', priveleges.ADMIN_PRIVELEGES, board)
        moder_group = create_group('Moderator', priveleges.MODER_PRIVELEGES, board)

        # Assign admin to current user
        user.groups.add(admin_group)
        user.save()
        
        # Success
        data = {
            'name' : board.name,
            'abbr' : board.abbr,
            'description' : board.description,
            'bump_limit' : board.bump_limit,
            'spam_words' : board.spam_words,
            'picture' : board.picture.url if board.picture else None,
            'author' : board.author.name,
            'created_at' : board.created_at.strftime('%d/%m/%Y %H:%M:%S')
        }

        return Response(data, status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

def add_priv_user(request, abbr, group_name, *args, **kwargs):
    if request.method == 'POST':
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

        # Check if user to be priveleged exists
        username = request.data.get('name')
        priv_user = models.User.objects.filter(name=username)
        if len(priv_user) == 0:
            message = {
                'message' : 'User with name {} doesn\'t exists.'.format(username)
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        priv_user = priv_user[0]

        # Success
        group = models.UserGroup.objects.filter(Q(name__icontains=group_name) & Q(board=board))[0]
        if user_priveleges['board'][0] is None:
            priv_user.groups.add(group)
            priv_user.save()

            message = {
                'message' : 'User {} became {} successfully!'.format(username, group_name)
            }
            return Response(message, status=status.HTTP_201_CREATED, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == board:
                    priv_user.groups.add(group)
                    priv_user.save()

                    message = {
                        'message' : 'User {} became {} successfully!'.format(username, group_name)
                    }
                    return Response(message, status=status.HTTP_201_CREATED, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to edit board /{}/.'.format(board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')