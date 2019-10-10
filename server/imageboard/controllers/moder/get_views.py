from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

# Helpers


# Views

def get_last_reports(request, *args, **kwargs):
    if request.method == 'GET':
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.object.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.GET_REPORTS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to view reports.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        data = []
        if user_priveleges[0]['board'] is None:
            reports = models.Report.objects.all().order_by('-created_at')
            for report in reports:
                data.append({
                    'post_id' : report.post.id,
                    'post_ip' : report.post.poster_ip,
                    'board' : report.post.thread.board.abbr, 
                    'reason' : report.reason,
                    'created_at' : report.created_at.strftime('%d/%m/%Y %H:%M:%S')
                })

        else:
            boards = []
            for privelege in user_priveleges:
                boards.append(privelege['board'])
            reports = models.Report.objects.filter(board__in=boards).order_by('-created_at')
            for report in reports:
                data.append({
                    'post_id' : report.post.id,
                    'post_ip' : report.post.poster_ip,
                    'board' : report.post.thread.board.abbr, 
                    'reason' : report.reason,
                    'created_at' : report.created_at.strftime('%d/%m/%Y %H:%M:%S')
                })
        
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')