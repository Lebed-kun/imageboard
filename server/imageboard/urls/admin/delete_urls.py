from django.urls import path

from ...controllers.admin import delete_views

urlpatterns = [
    path('deleteboard/<id>', delete_views.delete_board),
    path('removeprivuser/<abbr>/<group_name>/<id>/', delete_views.remove_priv_user)
]