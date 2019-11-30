from django.urls import path

from ...controllers.post import post_views

# Done!
urlpatterns = [
    path('feedback/', post_views.send_request_board),
    path('boards/<abbr>/create/', post_views.create_thread),
    path('threads/<thread_id>/create/', post_views.create_post),
    path('threads/<thread_id>/report/', post_views.report_posts)
]