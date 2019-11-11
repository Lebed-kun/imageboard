from django.urls import path

from ...controllers.moder import post_views

# Done!
urlpatterns = [
    path('new_ban/', post_views.ban_poster)
]