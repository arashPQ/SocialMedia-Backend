from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import api_view, authentication_classes, permission_classes


from account.forms import SignupForm, ProfileForm
from account.serializers import FollowRequestSerializer, UserSerializer
from account.models import User, FollowRequest
from account.utils import SendVerificationEmail
from notification.utils import create_notification



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64,).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your account is activated. Please login again")
        auth.logout(request)
        return redirect('account:token_obtain')
    
    else:
        messages.error(request, "Invalid activation link")
        return redirect('account:signup')



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
        user.is_active = False
        user.save()
        
        mail_subject = "Please Verify Your email"
        email_template = "account/emails/verification_email.html"
        SendVerificationEmail(request, user, mail_subject, email_template)
    # armanpq1990@gmail.com
        
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
    serializer = UserSerializer(request.user.people.all(), many=True)
    
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
    