from django.urls import path

from ...controllers.moder import put_views

# Done!
urlpatterns = [
    path('editpost/<id>/', put_views.edit_post),
    path('editthread/<id>/', put_views.edit_thread),
    path('editban/<id>/', put_views.edit_ban)
]