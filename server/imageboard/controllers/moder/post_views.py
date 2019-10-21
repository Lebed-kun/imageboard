from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

def ban_poster(request, *args, **kwargs):
    if request.method == 'POST':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if user has access to ban posters
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.BAN_POSTERS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to ban posters.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if board exists
        abbr = request.data.get('board', '')
        board = models.Board.objects.filter(abbr=abbr)
        if abbr == '':
            board = None
        elif len(board) == 0:
            message = {
                'message' : 'Board doesn\'t exist.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        else:
            board = board[0]

        # Success
        if user_priveleges[0]['board'] is None:
            ban = models.Ban.objects.create(**{
                'poster_ip' : request.data.get('poster_ip'),
                'expired_at' : request.data.get('expired_at'),
                'reason' : request.data.get('reason'),
                'board' : board
            })
            data = {
                'id' : ban.id,
                'poster_ip' : ban.poster_ip,
                'expired_at' : ban.expired_at,
                'reason' : ban.reason,
                'board' : '*' if ban.board is None else ban.board.abbr,
                'created_at' : ban.created_at.strftime('%d/%m/%Y %H:%M:%S')
            }
            return Response(data, status=status.HTTP_202_ACCEPTED, content_type='application/json')
        else:
            for priv in user_priveleges:
                if priv['board'] == board and board is not None:
                    ban = models.Ban.objects.create(**{
                        'poster_ip' : request.data.get('poster_ip'),
                        'expired_at' : request.data.get('expired_at'),
                        'reason' : request.data.get('reason'),
                        'board' : board
                    })
                    data = {
                        'id' : ban.id,
                        'poster_ip' : ban.poster_ip,
                        'expired_at' : ban.expired_at,
                        'reason' : ban.reason,
                        'board' : '*' if ban.board is None else ban.board.abbr,
                        'created_at' : ban.created_at.strftime('%d/%m/%Y %H:%M:%S')
                    }
                    return Response(data, status=status.HTTP_202_ACCEPTED, content_type='application/json')
            else:
                message = {
                    'message' : 'User doesn\'t have permission to ban users from board /{}/.'.format(board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, application='application/json')