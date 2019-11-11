from django.db.models import F
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status

from ... import models
from ... import constants
from ...utils import get_visitor_ip, full_text_found
from ..user.post_views import is_user_authorized
from ... import priveleges

# Helpers


# Views

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_last_reports(request, *args, **kwargs):
    if request.method == 'GET':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        # Check if user has access to read reports
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.GET_REPORTS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to view reports.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Success
        reports = None
        search_query = request.query_params.get('q', None)
        search_fields = request.query_params.get('fields', 'reason')
        search_fields = search_fields.split(',')
        if user_priveleges[0]['board'] is None:
            reports = models.Report.objects.all()
            if search_query is not None:
                reports = reports.filter(full_text_found(search_fields, search_query))
            reports = reports.order_by('-created_at')
        else:
            boards = []
            for privelege in user_priveleges:
                boards.append(privelege['board'])
            reports = models.Report.objects.filter(board__in=boards)
            if search_query is not None:
                reports = reports.filter(full_text_found('reason', search_query))
            reports = reports.order_by('-created_at')

        per_page = kwargs.get('per_page', constants.REPORTS_PER_PAGE)
        paginator = Paginator(reports, per_page)
        page = request.query_params.get('page', 1)
        page = paginator.page(page)

        reports = page.object_list

        data = {
            'pages_count' : paginator.num_pages,
            'prev_page' : page.previous_page_number() if page.has_previous() else None,
            'next_page' : page.next_page_number() if page.has_next() else None,
            'results' : []
        }

        for report in reports:
            data['results'].append({
                'id' : report.id,
                'post_id' : report.post.id,
                'post_ip' : report.post.poster_ip,
                'board' : report.post.thread.board.abbr, 
                'reason' : report.reason,
                'created_at' : report.created_at.strftime('%d/%m/%Y %H:%M:%S')
            })

        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_last_bans(request, *args, **kwargs):
    if request.method == 'GET':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if user has access to view bans
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.GET_BANS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to view bans.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Success
        bans = None
        search_query = request.query_params.get('q', None)
        search_fields = request.query_params.get('fields', 'reason')
        search_fields = search_fields.split(',')
        if user_priveleges[0]['board'] is None:
            bans = models.Ban.objects.all()
            if search_query is not None:
                bans = bans.filter(full_text_found(search_fields, search_query))
            bans = bans.order_by('-created_at')
        else:
            boards = []
            for privelege in user_priveleges:
                boards.append(privelege['board'])
            bans = models.Ban.objects.filter(board__in=boards)
            if search_query is not None:
                bans = bans.filter(full_text_found('reason', search_query))
            bans = bans.order_by('-created_at')

        per_page = kwargs.get('per_page', constants.BANS_PER_PAGE)
        paginator = Paginator(bans, per_page)
        page = request.query_params.get('page', 1)
        page = paginator.page(page)

        bans = page.object_list

        data = {
            'pages_count' : paginator.num_pages,
            'prev_page' : page.previous_page_number() if page.has_previous() else None,
            'next_page' : page.next_page_number() if page.has_next() else None,
            'results' : []
        }

        for ban in bans:
            data['results'].append({
                'id' : ban.id,
                'poster_ip' : ban.poster_ip,
                'expired_at' : ban.expired_at.strftime('%d/%m/%Y %H:%M:%S'),
                'reason' : ban.reason,
                'board' : '*' if ban.board is None else ban.board.abbr,
                'created_at' : ban.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'updated_at' : ban.updated_at.strftime('%d/%m/%Y %H:%M:%S')
            })

        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_moder_boards(request, *args, **kwargs):
    if request.method == 'GET':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Check if user has access to view moderated boards
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.GET_MODER_BOARDS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to view moderated boards.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # Success
        moder_boards = None
        search_query = request.query_params.get('q', None)
        search_fields = request.query_params.get('fields', 'name')
        search_fields = search_fields.split(',')
        if user_priveleges[0]['board'] is None:
            moder_boards = models.Board.objects.all()
            if search_query is not None:
                moder_boards = moder_boards.filter(full_text_found(search_fields, search_query))
        else:
            board_ids = []
            for privelege in user_priveleges:
                board_ids.append(privelege['board'].id)
            moder_boards = models.Board.objects.filter(id__in=board_ids)
            if search_query is not None:
                moder_boards = moder_boards.filter(full_text_found(search_fields, search_query))

        per_page = kwargs.get('per_page', constants.MODER_BOARDS_PER_PAGE)
        paginator = Paginator(moder_boards, per_page)
        page = request.query_params.get('page', 1)
        page = paginator.page(page)

        moder_boards = page.object_list

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
