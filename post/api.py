from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from post.models import Post
from post.serializers import PostSerializer

@api_view(['GET'])
def post_list(request):

    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    data = {
        'serializer': serializer.data
    }

    return JsonResponse(data)