from rest_framework import serializers

from notification.models import Notification
from account.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'body', 'type_of_notification', 'post_id', 'created_for_id')