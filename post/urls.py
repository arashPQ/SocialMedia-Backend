from django.urls import path

from post import api


urlpatterns = [
    path('', api.post_feed, name='post_feed'),
    path('profile/<str:uname>/', api.user_posts, name='user_posts'),
    path('create/', api.create_post, name='create_post'),
    
]
