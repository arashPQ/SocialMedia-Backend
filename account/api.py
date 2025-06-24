from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.conf import settings
from django.core.mail import EmailMessage


from account.forms import SignupForm, ProfileForm
from account.serializers import FollowRequestSerializer, UserSerializer
from account.models import User, FollowRequest
from notification.utils import create_notification


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'username': request.user.username,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
        
    })


@api_view(['POST'])
def editme(request):
    user = request.user
    email = request.data.get('email')
    username = request.data.get('username')
    
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists.'})
    if User.objects.exclude(id=user.id).filter(username=username).exists():
        return JsonResponse({'message': 'username already exists.'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            
        serializer = UserSerializer(user)
        
        data = {
            'message': 'profile information updated.',
            'user': serializer.data
        }
        return JsonResponse(data)        
    

@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(data=request.POST, user=user)
    
    if form.is_valid():
        form.save()
        
        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)
    
    


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
        user = form.save()
        # user.is_active = False
        user.save()
        
        
        # token = f'{settings.FAKE_SITE}/activatemail/?email={user.email}&id={user.id}'
        # mail_subject = "Please Verify Your email"
        # message = f"Verfify Your email address with : {token}"
        # from_email = settings.DEFAULT_FROM_EMAIL
        # to_email = user.email
        # mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
        # mail.send()
        
    else:
        message = form.errors.as_json()

    
    return JsonResponse({'message': message}, safe=False)



@api_view(['GET'])
def followers(request, pk):
    user = User.objects.get(pk=pk)
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


@api_view(['GET'])
def suggestion_people(request):
    serializer = UserSerializer(request.user.peoples.all(), many=True)
    
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def send_follow_request(request, pk):
    user = User.objects.get(pk=pk)

    check1 = FollowRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FollowRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        friendrequest = FollowRequest.objects.create(created_for=user, created_by=request.user)

        notification = create_notification(request, 'newfollowrequest', followrequest_id=friendrequest.id)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def handle_follow_request(request, status, pk):
    user = User.objects.get(pk=pk)

    follow_request = FollowRequest.objects.filter(created_for=request.user).get(created_by=user)
    follow_request.status = status
    follow_request.save()
    
    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    follower = request.user
    follower.friends_count = follower.friends_count + 1
    follower.save()
    
    notification = create_notification(request, 'acceptedfollowrequest', followrequest_id=follow_request.id)

    return JsonResponse({'message': 'follow request updated'})
    