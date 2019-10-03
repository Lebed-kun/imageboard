from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from datetime import datetime, timezone

from ... import models
from ... import constants
from ...utils import get_visitor_ip

# Helpers

def is_user_authorized(ip):
    token = models.UserToken.objects.filter(ip=ip)
    if len(token) == 0:
        return False
    token = token[0]

    user = models.User.objects.filter(token=token)[0]
    return user.is_authorized()

# Views


