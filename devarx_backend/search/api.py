from django.http import JsonResponse
from django.db.models import Q
from account.models import User
from post.models import Post
from account.serializers import UserSerializer
from post.serializers import PostSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# Create your views here.
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def searchUsers(request, query):
    users = User.objects.filter(Q (name__icontains = query ) | Q (email__icontains =query))
    posts = Post.objects.filter(Q (body__icontains = query ))
    serializedUsers = UserSerializer(users, many=True)
    serializedPosts = PostSerializer(posts, many=True)
    return JsonResponse({'users': serializedUsers.data, 'posts': serializedPosts.data })
