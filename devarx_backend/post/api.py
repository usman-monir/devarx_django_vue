from rest_framework.decorators import api_view, authentication_classes
from .models import Post
from account.models import User
from .forms import CreatePostForm
from django.http import JsonResponse
from .serializers import PostSerializer, UserSerializer
# Create your views here.

@api_view(['GET'])
def allPosts(request):
    all_users_ids = [str(request.user.id)]
    for user in request.user.friends.all():
        all_users_ids.append(str(user.id))
    posts = Post.objects.filter(created_by_id__in=all_users_ids)
    serializedPosts = PostSerializer(posts, many=True)
    return JsonResponse({'posts': serializedPosts.data})


@api_view(['POST'])
def createPost(request):
    data = request.data
    form = CreatePostForm(data)
    if form.is_valid():
        newPost = form.save(commit=False)
        newPost.created_by = request.user
        newPost.save()
        serializedPosts = PostSerializer(newPost)
        return JsonResponse({'newPost': serializedPosts.data})
    else:
        return JsonResponse({'newPost': None})


@api_view(['GET'])
def getUserPosts(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by=user)
    serializedPosts = PostSerializer(posts, many=True)
    serializedUser = UserSerializer(user)
    return JsonResponse({'posts': serializedPosts.data, 'user': serializedUser.data})
