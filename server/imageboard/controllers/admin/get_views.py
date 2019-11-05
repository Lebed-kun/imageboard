from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status

from ... import models
from ... import constants
from ...utils import get_visitor_ip, full_text_found
from ..user.post_views import is_user_authorized
from ... import priveleges

def get_admin_boards(request, *args, **kwargs):
    if request.method == 'GET':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Get view admin boards priveleges
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.GET_ADMIN_BOARDS)

        # Get boards
        boards = None
        search_query = request.query_params.get('q', None)
        search_fields = request.query_params.get('fields', 'name')
        search_fields = search_fields.split(',')
        if user_priveleges[0]['board'] is None:
            boards = models.Board.objects.all()
            if search_query is not None:
                boards = boards.filter(full_text_found(search_fields, search_query))
        else:
            board_ids = []
            for privelege in user_priveleges:
                board_ids.append(privelege['board'].id)
            boards = models.Board.objects.filter(id__in=board_ids)
            if search_query is not None:
                boards = boards.filter(full_text_found(search_fields, search_query))

        per_page = kwargs.get('per_page', constants.ADMIN_BOARDS_PER_PAGE)
        paginator = Paginator(boards, per_page)
        page = request.query_params.get('page', 1)
        page = paginator.page(page)
        boards = page.object_list

        data = {
            'pages_count' : paginator.num_pages,
            'prev_page' : page.previous_page_number() if page.has_previous() else None,
            'next_page' : page.next_page_number() if page.has_next() else None,
            'results' : []
        }

        for board in moder_boards:
            data['results'].append({
                'name' : board.name,
                'abbr' : board.abbr,
                'description' : board.description,
                'picture' : board.picture.url if board.picture else None,
                'author' : board.author.name if board.author else None,
                'created_at' : board.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'updated_at' : board.updated_at.strftime('%d/%m/%Y %H:%M:%S')
            })

        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

def get_priv_users(request, abbr, *args, **kwargs):
    if request.method == 'GET':
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

        # Success
        priv_users = None
        search_query = request.query_params.get('q', None)
        search_fields = request.query_params.get('fields', 'name')
        search_fields = search_fields.split(',')
        if user_priveleges[0]['board'] is None:
            # TO DO
            pass
        else:
            # TO DO
            pass
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')