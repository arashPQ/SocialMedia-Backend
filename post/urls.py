from django.urls import path

from post import api

app_name="post"

urlpatterns = [
    path('', api.post_feed, name='post_feed'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/add_comment/', api.add_comment, name='add_commnet'),
    path('profile/<uuid:id>/', api.user_posts, name='user_posts'),
    path('create/', api.create_post, name='create_post'),
    path('trends/', api.trends, name='trends')
    
]
