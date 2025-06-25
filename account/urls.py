from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account import api

app_name="account"

urlpatterns = [
    path('me/', api.me, name='me'),
    path('profile/edit/', api.editme, name='editme'),
    path('active/<uidb64>/<token>/', api.activate, name='activate'),
    path('profile/editpw/', api.edit_password, name='edit_password'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', api.signup, name='signup'),
    path('followers/<uuid:pk>/', api.followers, name='followers'),
    path('followers/suggested/', api.suggestion_people, name='suggestion_people'),
    path('followers/<uuid:pk>/<str:status>/', api.handle_follow_request, name='handle_follow_request'),
    path('followers/request/<uuid:pk>/', api.send_follow_request, name='sent_follow_request'),
    
]
