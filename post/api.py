from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User, FollowRequest
from account.serializers import UserSerializer
from post.models import Post, Like, Comment, Trends
from post.serializers import TrendsSerializer, PostSerializer, PostDetailSerializer, CommentSerializer
from post.forms import PostForm, AttachmentForm
from notification.utils import create_notification


@api_view(['GET'])
def post_feed(request):

    user_ids = [request.user.id]
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
        
        
    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')
    
    if trend: 
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_detail(request, pk):
    user_ids = [request.user.id]
    
    for user in request.user.friends.all():
        user_ids.append(user.id)
        
        
    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)
    
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
    
    notification = create_notification(request, 'postcomment', post_id=post.id)
    
    serializer = CommentSerializer(comment)
    
    return JsonResponse(serializer.data, safe=False)



@api_view(['POST'])
def create_post(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    
    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        
        
        if attachment:
            post.attachments.add(attachment)
            
            
        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()
        
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else: 
        return JsonResponse({
            'error': 'add something ...!'
        })
        
        
        
@api_view(['GET'])
def user_posts(request, id):
    posts = Post.objects.filter(created_by__id=id)
    user = User.objects.get(pk=id)
    
    if not request.user in user.friends.all():
        posts = posts.filter(is_private=False)
    
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    can_send_follow_req = True
    check1 = FollowRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FollowRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_follow_req = False
    data = {
        'posts': post_serializer.data,
        'user': user_serializer.data,
        'can_send_follow_req': can_send_follow_req
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
        
        notification = create_notification(request, 'postlike', post_id=post.id)
        return JsonResponse({'message': 'like created'})

    else:
        return JsonResponse({'message': 'post already liked.'})
    

@api_view(['GET'])
def trends(request):
    trends = Trends.objects.all()
    serializer = TrendsSerializer(Trends.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
def delete_post(request, id):
    post = Post.objects.filter(created_by=request.user).get(pk=id)
    post.delete()
    
    return JsonResponse({'message': 'post deleted.'})
    

@api_view(['POST'])
def report_post(request, id):
    post = Post.objects.get(pk=id)
    post.reported_by_people.add(request.user)
    post.save()
    
    return JsonResponse({'message': 'post reported.'})
    
    
