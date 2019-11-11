from django.urls import path

from ...controllers.post import get_views

urlpatterns = [
    path('', get_views.get_general_boards),
    path('userboards/', get_views.get_user_boards),
    path('boards/<abbr>', get_views.get_last_updated_threads),
    path('boards/<abbr>/<thread_id>', get_views.get_posts_list)
]