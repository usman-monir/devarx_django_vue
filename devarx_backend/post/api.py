from rest_framework.decorators import api_view, authentication_classes
from .models import Post
from .forms import CreatePostForm
from django.http import JsonResponse
from .serializers import PostSerializer
# Create your views here.

@api_view(['GET'])
def all_posts(request):
    posts = Post.objects.all()
    serialized_posts = PostSerializer(posts, many=True)
    return JsonResponse({'posts': serialized_posts.data})


@api_view(['POST'])
def create_post(request):
    data = request.data
    form = CreatePostForm(data)
    if form.is_valid():
        newPost = form.save(commit=False)
        newPost.created_by = request.user
        newPost.save()
        serialized_post = PostSerializer(newPost)
        return JsonResponse({'newPost': serialized_post.data})
    else:
        return JsonResponse({'newPost': None})
