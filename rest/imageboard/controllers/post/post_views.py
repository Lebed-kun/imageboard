from django.db.models import F
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from rest_framework import status
import base64
from datetime import datetime, timezone

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

    result = {}
    result['local'] = local_ban if local_ban is not None and\
        local_ban.expired_at >= datetime.now(timezone.utc) else None
    result['global'] = global_ban if global_ban is not None and\
        global_ban.expired_at >= datetime.now(timezone.utc) else None

    if local_ban is not None and result['local'] is None:
        local_ban.delete()
    if global_ban is not None and result['global'] is None:
        global_ban.delete()

    return result

def is_visitor_banned(global_ban, local_ban):
    return global_ban is not None or local_ban is not None

# Posting create views
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def create_post(request, thread_id, *args, **kwargs):
    if request.method == 'POST':
        thread = None
        try:
            thread = models.Thread.objects.get(id=thread_id)
        except models.Thread.DoesNotExist:
            message = {
                'message' : 'Thread not found.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        if thread.read_only:
            message = {
                'message' : 'Thread is read only!'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

        poster_ip = kwargs.get('poster_ip', get_visitor_ip(request))
        bans = get_bans(poster_ip, thread.board.abbr)
        banned = is_visitor_banned(bans['global'], bans['local'])

        if banned:
            ban = bans['local'] if bans['global'] is None else bans['global']

            data = {
                'banned' : True,
                'board' : '*' if ban.board is None else ban.board.abbr,
                'expired_at' : ban.expired_at.strftime('%d/%m/%Y %H:%M:%S'),
                'reason' : ban.reason
            }

            return Response(data, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        else:
            data = {
                'title' : request.data.get('title', ''),
                'author' : request.data.get('author', ''),
                'contact' : request.data.get('contact', ''),
                'options' : request.data.get('options', ''),
                'message' : request.data.get('message'),
                'poster_ip' : poster_ip,
                'thread' : thread
            }

            files = request.data.get('files', [])

            if len(files) > constants.MAX_FILES_COUNT:
                message = {
                    'message' : str(constants.MAX_FILES_COUNT) + ' files at most are allowed.'
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

            files_size = 0
            for f in files:
                files_size += (len(f['content']) * (3 / 4)) - 2
            if files_size > constants.MAX_FILES_SIZE:
                message = {
                    'message' : 'Files should be ' + str(constants.MAX_FILES_SIZE_MB) + \
                        ' MB in size at most.'
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN, content_type='application/json')

            post = models.Post.objects.create(**data)
            
            data['files'] = []
            for f in files:
                file_data = ContentFile(base64.b64decode(f['content']), name=f['name'])
                post_file = models.PostFile.objects.create(post_file=file_data, post=post)
                data['files'].append({
                    'name' : post_file.get_file_name(),
                    'url' : post_file.post_file.url
                })

            
            del data['poster_ip']
            data['thread'] = data['thread'].id
            data['created_at'] = post.created_at.strftime('%d/%m/%Y %H:%M:%S')
            data['id'] = post.id

            return Response(data, status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def report_posts(request, thread_id, *args, **kwargs):
    if request.method == 'POST':
        ids = request.data.get('ids')
        posts = []
        try:
            for id in ids:
                post = models.Post.objects.get(id=id)
                posts.append(post)
        except models.Post.DoesNotExist:
            message = {
                'message' : 'Post not found.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        data = {
            'reason' : request.data.get('reason'),
            'posts' : posts
        }

        for post in data['posts']:
            models.Report.objects.create(post=post, board=post.thread.board, reason=data['reason'])
        
        message = {
            'message' : 'Report succeed.'
        }

        return Response(message, status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def create_thread(request, abbr, *args, **kwargs):
    if request.method == 'POST':
        board = models.Board.objects.filter(abbr=abbr)
        if len(board) < 1:
            message = {
                'message' : 'Board not found.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        board = board[0]

        poster_ip = kwargs.get('poster_ip', get_visitor_ip(request))
        bans = get_bans(poster_ip, abbr)
        banned = is_visitor_banned(bans['global'], bans['local'])

        if banned:
            ban = bans['local'] if bans['global'] is None else bans['global']

            data = {
                'banned' : True,
                'board' : '*' if ban.board is None else ban.board.abbr,
                'expired_at' : ban.expired_at.strftime('%d/%m/%Y %H:%M:%S'),
                'reason' : ban.reason
            }

            return Response(data, status=status.HTTP_403_FORBIDDEN, content_type='application/json')
        
        thread = models.Thread.objects.create(board=board)
        create_post(request._request, thread.id, *args, **kwargs)

        data = {
            'created' : True,
            'id' : thread.id
        }

        return Response(data, status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def send_request_board(request, *args, **kwargs):
    if request.method == 'POST':
        subject = request.data['subject']
        text = request.data['text']
        
        board_request = models.Requests.objects.create(subject=subject, text=text)

        return Response(status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
