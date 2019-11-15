from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes

from ... import models
from ... import constants
from ...utils import get_visitor_ip, full_text_found
from ..user.post_views import is_user_authorized
from ... import priveleges

# Helpers

def get_priv_users_data(group, board, search=None):
    data = []
    
    group = models.UserGroup.objects.filter(Q(name__icontains=group) & Q(board=board))[0]
    priv_users = models.User.objects.filter(groups=group)
    if search is not None and search.get('query', None) is not None:
        priv_users = priv_users.filter(full_text_found(search['fields'], search['query']))

    for user in priv_users:
        data.append({
            'name' : user.name,
            'created_at' : user.created_at.strftime('%d/%m/%Y %H:%M:%S'),
            'updated_at' : user.updated_at.strftime('%d/%m/%Y %H:%M:%S')
        })

    return data    

# Views

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
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

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_priv_users(request, abbr, group_name, *args, **kwargs):
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
        board = board[0]

        # Success
        group = group_name
        priv_users = None
        search_query = request.query_params.get('q', None)
        search_fields = request.query_params.get('fields', 'name')
        search_fields = search_fields.split(',')

        data = []
        if user_priveleges[0]['board'] is None:
            data = get_priv_users_data(group, board, {
                'fields' : search_fields,
                'query' : search_query
            })
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')            
        else:
            for priv in user_priveleges:
                if priv['board'] == board:
                    data = get_priv_users_data(group, board, {
                        'fields' : search_fields,
                        'query' : search_query
                    })
                    return Response(data, status=status.HTTP_200_OK, content_type='application/json')  
            else:
                message = {
                    'message' : 'User doesn\'t have permission to edit board /{}/.'.format(board.abbr)
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')