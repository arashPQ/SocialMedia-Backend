from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.serializers import UserSerializer
from account.models import User

from post.models import Post
from post.serializers import PostSerializer


@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    user_ids = [request.user.id]

    # for user in request.user.friends.all():
    #     user_ids.append(user.id)

    users = User.objects.filter(username__icontains=query)
    users_serializer = UserSerializer(users, many=True)

    posts = Post.objects.filter(
        Q(body__icontains=query) | 
        Q(created_by_id__in=list(user_ids), body__icontains=query)
    )

    posts_serializer = PostSerializer(posts, many=True)

    data = {
        'users': users_serializer.data,
        'posts': posts_serializer.data
    }
    
    return JsonResponse(data, safe=False)