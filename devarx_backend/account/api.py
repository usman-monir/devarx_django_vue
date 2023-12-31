from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import User, FriendRequest
from .serializers import RequestsSerializer, UserSerializer
from .forms import SignupForm


@api_view(['GET'])
def user(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
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
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })
    if form.is_valid():
        form.save()
        # send verification email
    else:
        message = 'error'

    return JsonResponse({'status': message})

@api_view(['POST'])
def editProfile(request):

    # getting form data
    name = request.data.get('name')
    email = request.data.get('email')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    avatar = request.data.get('avatar')

    print(request.FILES)

    # status
    FAILURE = 'failure'
    SUCCESS = 'success'
    status = SUCCESS
    message = 'Couldn\'t update user!! Something happened unexpected!'

    # saving new attributes
    request.user.name = name
    emailAlreadyExists = User.objects.exclude(id=request.user.id).filter(email=email)
    if emailAlreadyExists:
        status = FAILURE
        message = 'Email already exists!'
    else:
        request.user.email = email
        # check for password
        if old_password:
            if check_password(old_password, request.user.password):
                request.user.set_password(new_password)
            else:
                status = FAILURE
                message = 'Passwords mismatched!'

    if avatar:
        request.user.avatar = avatar

    if status == SUCCESS:
        message = 'User updated successfully'
        request.user.save()
    else:
        print('user is not updated!')
    return JsonResponse({'status': status, 'message': message, 'avatar': request.user.get_avatar()})



@api_view(['POST'])
def sendFriendRequest(request):
    user_id = request.data.get('id')
    user = User.objects.get(pk=user_id)

    alreadySent = FriendRequest.objects.filter( Q (send_by=request.user) | Q( send_to=user))
    if alreadySent:
        return JsonResponse({'status': 'Request already sent!'})
    if user != request.user:
        FriendRequest.objects.create(send_by=request.user, send_to= user)
        return JsonResponse({'status': 'request sent!'})


@api_view(['POST'])
def unFriend(request):
    user_id = request.data.get('id')
    user = User.objects.get(pk=user_id)
    request.user.friends.remove(user)
    user.friends.remove(request.user)
    return JsonResponse({'status': 'Removed from friends list!'})


@api_view(['GET'])
def getCurrentUserFriendsData(request):
    requests = FriendRequest.objects.filter(send_to=request.user)
    friends = request.user.friends.all()
    requests= RequestsSerializer(requests, many=True)
    friends = UserSerializer(friends, many=True)
    return JsonResponse({'friendRequests': requests.data, 'friends': friends.data})


@api_view(['POST'])
def acceptFriendRequest(request):
    user = User.objects.get(pk=request.data.get('id'))
    request.user.friends.add(user)
    friendRequest1 = FriendRequest.objects.filter(Q(send_by=user) & Q(send_to=request.user))
    friendRequest2 = FriendRequest.objects.filter(Q(send_by=request.user) & Q(send_to=user))
    friendRequest1.delete()
    if friendRequest2:
        friendRequest2.delete()

    return JsonResponse({'status': 'Added to the friends list!'})


@api_view(['POST'])
def rejectFriendRequest(request):
    user = User.objects.get(pk=request.data.get('id'))
    friendRequest1 = FriendRequest.objects.filter(Q(send_by=user) & Q(send_to=request.user))
    friendRequest2 = FriendRequest.objects.filter(Q(send_by=request.user) & Q(send_to=user))
    friendRequest1.delete()
    if friendRequest2:
        friendRequest2.delete()

    return JsonResponse({'status': 'Removed from the friend requests!'})


@api_view(['GET'])
def getViewedUserFriendsData(request, user_id):
    user = User.objects.get(pk=user_id)
    friends = user.friends.all()
    mutualFriends = request.user.friends.filter(pk__in=friends)
    friends = UserSerializer(friends, many=True)
    mutualFriends = UserSerializer(mutualFriends, many=True)
    return JsonResponse({'friends': friends.data, 'mutualFriends': mutualFriends.data })


@api_view(['GET'])
def suggestedPeople(request):
    friends = request.user.friends.all()
    suggestedPeople = User.objects.exclude(pk__in=friends).exclude(pk=request.user.id)[:5]
    suggestedPeople = UserSerializer(suggestedPeople, many=True)
    return JsonResponse({'suggestedPeople': suggestedPeople.data})
