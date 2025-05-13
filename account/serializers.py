from rest_framework import serializers

from account.models import User, FollowRequest


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email', 'friends_count')
        
        
class FollowRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = FollowRequest
        fields = ('id', 'created_by')
