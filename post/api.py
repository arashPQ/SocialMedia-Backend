from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from post.models import Post
from post.serializers import PostSerializer
from post.forms import PostForm



@api_view(['GET'])
def post_list(request):

    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def create_post(request):
    form = PostForm(request.data)
    
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else: 
        return JsonResponse({
            'error': 'add something ...!'
        })