from django.urls import path

from ...controllers.moder import get_views

urlpatterns = [
    path('reports/', get_views.get_last_reports),
    path('bans/', get_views.get_last_bans),
    path('boards/', get_views.get_moder_boards)
]