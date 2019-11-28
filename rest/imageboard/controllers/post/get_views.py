from django.db.models import F
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes

from ... import models
from ... import constants
from ...utils import full_text_found

def get_post_data(post):
    data = {
        'id' : post.id,
        'title' : post.title,
        'author' : post.author,
        'contact' : post.contact,
        'options' : post.options,
        'message' : post.message,
        'created_at' : post.created_at.strftime('%d/%m/%Y %H:%M:%S'),
        'updated_at' : post.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
        'files' : []
    }

    files = models.PostFile.objects.filter(post=post)
    for post_file in files:
        data['files'].append({
            'name' : post_file.post_file.get_file_name(),
            'url' : post_file.post_file.url
        })
    
    return data

# Views

# General

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_site_info(request, *args, **kwargs):
    if request.method == 'GET':
        info = None
        try:
            info = models.SiteInfo.objects.get(id=1)
            data = {
                'info' : info.info,
                'created_at' : info.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'updated_at' : info.updated_at.strftime('%d/%m/%Y %H:%M:%S')
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        except models.SiteInfo.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_general_boards(request, *args, **kwargs):
    if request.method == 'GET':
        boards = models.Board.objects.filter(author=None)

        data = []
        for board in boards:
            data.append({
                'name' : board.name,
                'abbr' : board.abbr
            })
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_last_updated_threads(request, abbr, *args, **kwargs):
    if request.method == 'GET':
        board = models.Board.objects.filter(abbr=abbr)
        if len(board) == 0:
            message = {
                'message' : 'Board not found.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
        board = board[0]

        threads = models.Thread.objects.filter(board=board)
        threads = threads.order_by('-sticked', '-bumped_at')

        query = request.query_params.get('q', None)
        query_threads = None
        if query is not None:
            query_threads = []
            query = query.split('+')
            for thread in threads:
                posts = models.Post.objects.filter(thread=thread)
                condition = Q(title__iregex='(' + '|'.join(query) + ')')
                posts = posts.filter(condition)
                if len(posts) > 0:
                    query_threads.append(posts[0].thread)
        
        if query_threads is not None:
            threads = query_threads

        per_page = kwargs.get('per_page', constants.THREADS_PER_PAGE)
        paginator = Paginator(threads, per_page)
        page = request.query_params.get('page', 1)
        page = paginator.page(page)

        threads = page.object_list
        data = {
            'pages_count' : paginator.num_pages,
            'prev_page' : page.previous_page_number() if page.has_previous() else None,
            'next_page' : page.next_page_number() if page.has_next() else None,
            'results' : []
        }
        for thread in threads:
            first_post = thread.first_post
            last_posts = models.Post.objects.filter(Q(thread=thread) & ~Q(id=first_post.id))
            posts_count = kwargs.get('posts_count', constants.LAST_POSTS_COUNT)
            last_posts = last_posts.order_by('-created_at')[:posts_count]

            thread_data = {
                'id' : thread.id,
                'sticked' : thread.sticked,
                'read_only' : thread.read_only,
                'first_post' : get_post_data(first_post),
                'last_posts' : []
            }

            for post in last_posts:
                thread_data['last_posts'].append(
                    get_post_data(post)
                )
            
            data['results'].append(thread_data)
        
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_posts_list(request, abbr, thread_id, *args, **kwargs):
    if request.method == 'GET':
        thread = None
        try:
            thread = models.Thread.objects.get(id=thread_id)
        except models.Thread.DoesNotExist:
            message = {
                'message' : 'Thread not found.'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND, content_type='application/json')

        posts = models.Post.objects.filter(thread=thread)

        data = []
        for post in posts:
            post_data = get_post_data(post)
            data.append(post_data)

        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

# User boards

@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def get_user_boards(request, *args, **kwargs):
    if request.method == 'GET':
        search_query = request.query_params.get('q', None)
        search_fields = request.query_params.get('fields', 'name')
        search_fields = search_fields.split(',')
        
        boards = models.Board.objects.filter(author__isnull=False)
        if search_query is not None:
            boards = boards.filter(full_text_found(search_fields, search_query))
        boards = boards.order_by('-created_at')

        per_page = kwargs.get('per_page', constants.BOARDS_PER_PAGE)
        paginator = Paginator(boards, per_page)
        page = request.query_params.get('page', 1)
        page = paginator.page(page)

        boards = page.object_list
        data = {
            'pages_count' : paginator.num_pages,
            'prev_page' : page.previous_page_number() if page.has_previous() else None,
            'next_page' : page.next_page_number() if page.has_next() else None,
            'results' : []
        }
        for board in boards:
            board_data = {
                'name' : board.name,
                'abbr' : board.abbr,
                'description' : board.description,
                'picture' : board.picture.url if board.picture else None,
                'author' : board.author.name,
                'created_at' : board.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'updated_at' : board.updated_at.strftime('%d/%m/%Y %H:%M:%S')
            }
            data['results'].append(board_data)

        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST, content_type='application/json')