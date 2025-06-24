from django.urls import path

from notification import api


urlpatterns = [
    path('', api.notifications, name='notifications'),
    path('<uuid:pk>/read/', api.read_notification, name='read_notification')
]
