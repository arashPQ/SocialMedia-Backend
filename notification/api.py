from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from notification.serilizers import NotificationSerializer
from notification.models import Notification
from notification.utils import get_notif_count

@api_view(['GET'])
def notifications(request):
    received_notifications = get_notif_count(request)
    serializer = NotificationSerializer(received_notifications, many=True)
    
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def read_notification(request, pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()
    
    return JsonResponse({'message': 'notification read'})