from django.urls import path

from post import api


urlpatterns = [
    path('', api.post_list, name='post_list')
]
