from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from rest_framework import status
import base64

from ... import models
from ... import constants
from ...utils import get_visitor_ip

# Check ban methods
def get_bans(visitor_ip, abbr):
    board = models.Board.objects.filter(abbr=abbr)[0]

    ban = models.Ban.objects.filter(poster_ip=visitor_ip, board=board)
    local_ban = ban[0] if len(ban) != 0 else None

    ban = models.Ban.objects.filter(poster_ip=visitor_ip, board=None)
    global_ban = ban[0] if len(ban) != 0 else None

    return {
        'global' : global_ban,
        'local' : local_ban
    }

def is_visitor_banned(global_ban, local_ban):
    return global_ban is not None or local_ban is not None

# Posting create views
def create_post(request, abbr, thread_id, *args, **kwargs):
    if request.method == 'POST':
        poster_ip = kwargs.get('poster_ip', get_visitor_ip(request))
        bans = get_bans(poster_ip, abbr)
        banned = is_visitor_banned(bans['global'], bans['local'])

        if banned:
            ban = bans['local'] if bans['global'] is None else bans['global']

            data = {
                'banned' : True,
                'board' : '*' if ban.board is None else ban.board.abbr,
                'expired_at' : ban.expired_at,
                'reason' : ban.reason
            }

            return Response(data, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        else:
            thread = models.Thread.objects.get(id=thread_id)
            
            data = {
                'title' : request.data.get('title', ''),
                'author' : request.data.get('author', ''),
                'contact' : request.data.get('contact', ''),
                'options' : request.data.get('options', ''),
                'message' : request.data.get('message'),
                'poster_ip' : poster_ip,
                'thread' : thread
            }
            post = models.Post.objects.create(**data)
            
            data['files'] = []
            files = request.data.get('files')
            for f in files:
                file_data = ContentFile(base64.b64decode(f['content']), name=f['name'])
                post_file = models.PostFile.objects.create(post_file=file_data, post=post)
                data['files'].append({
                    'name' : post_file.get_file_name(),
                    'url' : post_file.post_file.url
                })
            
            del data['poster_ip']
            data['created_at'] = post.created_at

            return Response(data, status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')