from django.urls import path

from ...controllers.user import post_views

urlpatterns = [
    path('authorize/', post_views.authorize),
    path('deauthorize/', post_views.deauthorize),
    path('register/', post_views.register)
]