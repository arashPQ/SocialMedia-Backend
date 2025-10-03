from rest_framework import serializers
from django.core.validators import RegexValidator
from account.models import User, FollowRequest


user_validator = RegexValidator(
    regex = r'^[a-zA-Z0-9_]+$',
    message = "username just can be a-z, A-Z, _"
)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'get_avatar', 'email', 'friends_count', 'posts_count')
        
        
class FollowRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = FollowRequest
        fields = ('id', 'created_by')
