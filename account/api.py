from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.forms import SignupForm
from account.serializers import FollowRequestSerializer, UserSerializer
from account.models import User, FollowRequest

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'username': request.user.username,
        'email': request.user.email,
        
    })



@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'username': data.get('username'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
        
    })
    
    if form.is_valid():
        form.save()
        
        # Send verification email
    else:
        message = 'error'
    
    return JsonResponse({'messsage': message})



@api_view(['GET'])
def followers(request, uname):
    user = User.objects.get(username=uname)
    requests = []

    if user == request.user:
        requests = FollowRequest.objects.filter(created_for=request.user, status=FollowRequest.SENT)
        requests = FollowRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    data = {
        'user': UserSerializer(user).data,
        'followers': UserSerializer(friends, many=True).data,
        'requests': requests
    }

    return JsonResponse(data, safe=False)




@api_view(['POST'])
def send_follow_request(request, uname):
    user = User.objects.get(username=uname)
    print(user)

    check1 = FollowRequest.objects.filter(created_by=request.user).filter(created_for=user)
    check2 = FollowRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        friendrequest = FollowRequest.objects.create(created_for=user, created_by=request.user)

        # notification = FollowRequest(request, 'new_friendrequest', friendrequest_id=friendrequest.id)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def handle_follow_request(request, status, pk):
    user = User.objects.get(pk=pk)
    print(user.pk)
    follow_request = FollowRequest.objects.filter(created_for=request.user).get(created_by=user)
    follow_request.status = status
    follow_request.save()
    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    follower = request.user
    follower.friends_count = follower.friends_count + 1
    follower.save()
    
    return JsonResponse({'message': 'follow request updated'})
    