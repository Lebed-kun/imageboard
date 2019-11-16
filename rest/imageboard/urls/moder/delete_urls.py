from django.urls import path

from ...controllers.moder import delete_views

urlpatterns = [
    path('deletereport/<id>/', delete_views.delete_report),
    path('deletepost/<id>/', delete_views.delete_post),
    path('deletethread/<id>/', delete_views.delete_thread),
    path('deleteban/<id>/', delete_views.delete_ban)
]