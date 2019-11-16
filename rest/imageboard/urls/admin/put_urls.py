from django.urls import path

from ...controllers.admin import put_views

urlpatterns = [
    path('editboard/<id>/', put_views.edit_board)
]