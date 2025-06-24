from django.db import models
import uuid

from account.models import User
from post.models import Post


class Notification(models.Model):
    NEWFOLLOWREQUEST = 'newfollowrequest'
    ACCEPEDTFOLLOWREQUEST = 'acceptedfollowrequest'
    REJECTEDFOLLOWREQUEST = 'rejectedfollowrequest'
    POST_LIKE = 'postlike'
    POST_COMMENT = 'postcomment'
    
    CHOICES_TYPE_OF_NOTIFICATION = {
        (NEWFOLLOWREQUEST, 'New followrequest'),
        (ACCEPEDTFOLLOWREQUEST, 'Accepted followrequest'),
        (REJECTEDFOLLOWREQUEST, 'Rejected followrequest'),
        (POST_LIKE, 'Post like'),
        (POST_COMMENT, 'Post comment')
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    created_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    