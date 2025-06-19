from django.urls import path

from chat import api

urlpatterns = [
    path('', api.conversation_list, name='conversation_list'),
    path('<uuid:pk>/', api.conversation_detail, name='conversation_detail'),
    path('<uuid:pk>/send/', api.conversation_send_message, name='conversation_send_message'),
    path('<str:uname>/direct/', api.conversation_get_or_create, name='conversation_send_message'),

]
