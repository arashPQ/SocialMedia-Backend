import uuid
from django.db import models
from django.utils.timesince import timesince
from django.conf import settings

from account.models import User


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def created_at_formatted(self):
        return timesince(self.created_at)

class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

    def get_image(self):
        if self.image:
            return settings.FAKE_SITE + self.image.url
        else:
            return ''

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    reported_by_people = models.ManyToManyField(User, blank=True)
    class Meta:
        ordering = ('-created_at',)
        
    def created_at_formatted(self):
        return timesince(self.created_at)
    
class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('created_by', 'post')


class Trends(models.Model):
    title = models.CharField(max_length=256)
    accurences = models.IntegerField()