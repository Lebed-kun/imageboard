from django.db.models import F
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .. import models
from .. import constants

def get_post_data(post):
    data = {
        'title' : post.title,
        'author' : post.author,
        'contact' : post.contact,
        'options' : post.options,
        'message' : post.message,
        'created_at' : post.created_at,
        'updated_at' : post.updated_at
    }
    files = models.PostFile.objects.filter(post=post)
    if len(files) > 0:
        data['files'] = []
        for post_file in files:
            data['files'].append({
                'name' : post_file.name,
                'url' : post_file.url
            })
    return data

# Views

def get_general_boards(self, request, *args, **kwargs):
    if request.method == 'GET':
        boards = models.Board.objects.filter(author=None)

        data = []
        for board in boards:
            data.append({
                'name' : board.name,
                'abbr' : board.abbr
            })
            
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

def get_last_updated_threads(self, request, abbr, *args, **kwargs):
    if request.method == 'GET':
        board = models.Board.objects.filter(abbr=abbr)
        if len(board) == 0:
            message = {
                'message' : 'Board not found'
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        board = board[0]

        threads = models.Thread.objects.filter(board=board)
        threads = threads.order_by('-bumped', '-updated_at')

        paginator = Paginator(threads, constants.THREADS_PER_PAGE)
        page = request.GET.get('page', 1)
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
            last_posts = models.Post.objects.filter(thread=thread)
            last_posts = last_posts.order_by('-created_at')[:constants.LAST_POSTS_COUNT]

            thread_data = {
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
        
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)