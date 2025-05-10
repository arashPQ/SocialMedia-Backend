from django.contrib import admin

from post.models import Post, PostAttachment

admin.site.register(Post)
admin.site.register(PostAttachment)
