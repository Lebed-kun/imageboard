from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized

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

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')