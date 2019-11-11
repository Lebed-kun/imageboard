from django.urls import path, include

urlpatterns = [
    path('main_get/', include('imageboard.urls.post.get_urls')),
    path('main_post/', include('imageboard.urls.post.post_urls'))
]