from rest_framework.response import Response
from django.core.files.base import ContentFile
from rest_framework import status
from datetime import datetime, timezone

from ... import models
from ... import constants

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
                'message' : 'Post doesn\'t exist.'
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