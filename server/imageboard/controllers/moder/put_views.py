from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from rest_framework import status
import base64
from datetime import datetime, timezone

from ... import models
from ... import constants
from ...utils import get_visitor_ip

def edit_post(request, id, *args, **kwargs):
    if request.method == 'PUT':
        # Check if user is authorized
        ip = kwargs.get('ip', get_visitor_ip(request))
        if not is_user_authorized(ip):
            message = {
                'message' : 'User is not authorized.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        # Check if user has access to delete posts
        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]
        user_priveleges = user.get_priveleges(priveleges.EDIT_POSTS)
        if len(user_priveleges) == 0:
            message = {
                'message' : 'User doesn\'t have permission to edit posts.'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        # TODO...
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')