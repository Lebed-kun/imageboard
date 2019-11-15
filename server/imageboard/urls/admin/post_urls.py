from django.urls import path

from ...controllers.admin import post_views

urlpatterns = [
    path('newboard/', post_views.create_board),
    path('addprivuser/', post_views.add_priv_user)
]