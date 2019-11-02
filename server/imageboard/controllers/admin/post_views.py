from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from django.core.files.base import ContentFile
import base64
from django.db import IntegrityError

from ... import models
from ... import constants
from ...utils import get_visitor_ip
from ..user.post_views import is_user_authorized
from ... import priveleges

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
        picture = request.data.get('picture', None)
        if picture is not None:
            picture = ContentFile(base64.b64decode(picture['content'], name=pucture['name']))

        token = models.UserToken.objects.filter(ip=ip)[0]
        user = models.User.objects.filter(token=token)[0]

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
        # TO DO
        pass
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')