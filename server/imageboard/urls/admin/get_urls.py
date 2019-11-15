from django.urls import path

from ...controllers.admin import get_views

urlpatterns = [
    path('adminboards/', get_views.get_admin_boards),
    path('privusers/', get_views.get_priv_users)
]