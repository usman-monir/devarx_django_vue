from rest_framework.decorators import api_view, authentication_classes
from .models import Post, Comment, Trend
from account.models import User
from .forms import CreatePostForm, PostAttachmentForm
from django.http import JsonResponse
from .serializers import PostSerializer, UserSerializer, TrendSerializer
# Create your views here.

@api_view(['GET'])
def allPosts(request):
    trend = request.GET.get('trend')

    if trend:
        posts = Post.objects.filter(body__icontains= '#' + trend)
    else:
        all_users_ids = [str(request.user.id)]
        for user in request.user.friends.all():
            all_users_ids.append(str(user.id))
        posts = Post.objects.filter(created_by_id__in=all_users_ids)

    serializedPosts = PostSerializer(posts, many=True)
    return JsonResponse({'posts': serializedPosts.data})


@api_view(['POST'])
def createPost(request):
    attachment= None
    postForm = CreatePostForm(request.POST)
    attachmentForm = PostAttachmentForm(request.POST, request.FILES)

    if attachmentForm.is_valid():
        attachment = attachmentForm.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if postForm.is_valid():
        newPost = postForm.save(commit=False)
        newPost.created_by = request.user
        newPost.save()

    if attachment:
        newPost.attachments.add(attachment)

    serializedPosts = PostSerializer(newPost)
    return JsonResponse({'newPost': serializedPosts.data})


@api_view(['GET'])
def getUserPosts(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by=user)
    serializedPosts = PostSerializer(posts, many=True)
    serializedUser = UserSerializer(user)
    return JsonResponse({'posts': serializedPosts.data, 'user': serializedUser.data})


@api_view(['POST'])
def likePost(request, id):
    postId = request.data.get('postId')
    post = Post.objects.get(pk=postId)
    post.likes.add(request.user)
    post.save()
    post = PostSerializer(post)
    return JsonResponse({'post': post.data})


@api_view(['POST'])
def dislikePost(request, id):
    postId = request.data.get('postId')
    post = Post.objects.get(pk=postId)
    post.likes.remove(request.user)
    post.save()
    post = PostSerializer(post)
    return JsonResponse({'post': post.data})


@api_view(['POST'])
def comment(request, id):
    body = request.data.get('body')
    postId = request.data.get('postId')
    post = Post.objects.get(pk=postId)
    comment = Comment.objects.create(body = body, created_by = request.user)
    if comment:
        post.comments.add(comment)
        post.save()
        post = PostSerializer(post)
        return JsonResponse({'post': post.data})
    return JsonResponse({'post': {}})


@api_view(['POST'])
def deleteComment(request, id):
    postId = request.data.get('postId')
    commentId = request.data.get('commentId')
    post = Post.objects.get(pk=postId)
    comment = post.comments.get(pk=commentId)
    if comment:
        post.comments.remove(comment)
        post.save()
        post = PostSerializer(post)
        return JsonResponse({'post': post.data})
    return JsonResponse({'post': {}})


@api_view(['POST'])
def editComment(request, id):
    postId = request.data.get('postId')
    commentBody = request.data.get('body')
    commentId = request.data.get('commentId')
    post = Post.objects.get(pk=postId)
    post.comments.filter(pk=commentId).update(body=commentBody)
    post.save()
    post = PostSerializer(post)
    return JsonResponse({'post': post.data})


@api_view(['POST'])
def deletePost(request, id):
    post = Post.objects.get(id=id)
    attachment = post.attachments.all()
    if attachment:
        attachment.delete()
    post.delete()
    return JsonResponse({'message': 'Post deleted successfully'})

@api_view(['POST'])
def editPost(request, id):
    post = Post.objects.get(id=id)
    post.body = request.data.get('body')
    post.save()
    post = PostSerializer(post)
    return JsonResponse({'post': post.data})

@api_view(['GET'])
def getTrends(request):
    trends = Trend.objects.all()
    trends = TrendSerializer(trends, many=True)
    return JsonResponse({'trends': trends.data})


