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

def get_own_boards(request, *args, **kwargs):
    pass

