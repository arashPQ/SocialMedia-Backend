from django.urls import path

from post import api


urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.create_post, name='create_post'),
    
]
