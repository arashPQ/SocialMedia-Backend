from rest_framework import serializers

from post.models import Post, PostAttachment, Comment, Trends, Like
from account.serializers import UserSerializer


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'is_liked', 'comments_count', 'created_by', 'created_at_formatted', 'attachments', 'is_private')

    def get_is_liked(self, post):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(created_by=request.user, post=post).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted')


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'comments', 'likes_count', 'comments_count', 'created_by', 'created_at_formatted', 'attachments')
        

class TrendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trends
        fields = ('id', 'title', 'accurences', )