from django.urls import path

from ...controllers.moder import post_views

# Done!
urlpatterns = [
    path('newban/', post_views.ban_poster)
]