from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', api.signup, name='signup'),
    path('followers/<str:uname>/', api.followers, name='followers'),
    path('followers/<uuid:pk>/<str:status>/', api.handle_follow_request, name='handle_follow_request'),
    path('followers/request/<str:uname>/', api.send_follow_request, name='sent_follow_request'),
    
]
