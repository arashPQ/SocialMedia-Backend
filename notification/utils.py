from notification.models import Notification
from post.models import Post
from account.models import FollowRequest



def create_notification(request, type_of_notification, followrequest_id=None, post_id=None):
    created_for = None
    if type_of_notification == 'postlike':
        body = f'{request.user.name} liked your post!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
        
    elif type_of_notification == 'postcomment':
        body = f'{request.user.name} commented on your post!'
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by
        
    elif type_of_notification == 'newfollowrequest':
        followrequest = FollowRequest.objects.get(pk=followrequest_id)
        created_for = followrequest.created_for
        body = f'{request.user.name} sent you follow request!'
        
    elif type_of_notification == 'acceptedfollowrequest':
        followrequest = FollowRequest.objects.get(pk=followrequest_id)
        created_for = followrequest.created_for
        body = f'{request.user.name} accepted you follow request!'
        
    elif type_of_notification == 'rejectedfollowrequest':
        followrequest = FollowRequest.objects.get(pk=followrequest_id)
        created_for = followrequest.created_for
        body = f'{request.user.name} rejected you follow request!'
    
    notification = Notification.objects.create(
        body=body,
        type_of_notification=type_of_notification,
        post_id=post_id,
        created_by = request.user,
        created_for=created_for
        
    )
    
    return notification