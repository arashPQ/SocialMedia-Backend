from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from post.models import Post, Like, Comment
from post.serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from post.forms import PostForm



@api_view(['GET'])
def post_feed(request):

    user_ids = [request.user.id]
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
        
        
    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['POST'])
def add_comment(request, pk):
    comment_body = request.data.get('body')
    comment = Comment.objects.create(body=comment_body, created_by=request.user)
    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()
    
    serializer = CommentSerializer(comment)
    
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
        
        
        
@api_view(['GET'])
def user_posts(request, uname):

    posts = Post.objects.filter(created_by__username=uname)
    user = User.objects.get(username=uname)
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    
    data = {
        'posts': post_serializer.data,
        'user': user_serializer.data
    }

    return JsonResponse(data, safe=False)


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()
    
        return JsonResponse({'message': 'like created'})

    else:
        return JsonResponse({'message': 'post already liked.'})