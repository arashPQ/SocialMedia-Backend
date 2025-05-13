from django.urls import path

from search import api

urlpatterns = [
    path('', api.search, name='search')
]
