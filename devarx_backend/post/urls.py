from django.urls import path
from . import api

urlpatterns = [
    path('', api.allPosts, name='allPosts'),
    path('profile/<uuid:id>/', api.getUserPosts, name='getUserPosts'),
    path('profile/<uuid:id>/likePost/', api.likePost, name='likePost'),
    path('profile/<uuid:id>/dislikePost/', api.dislikePost, name='dislikePost'),
    path('profile/<uuid:id>/comment/', api.comment, name='comment'),
    path('profile/<uuid:id>/comment/delete', api.deleteComment, name='deleteComment'),
    path('profile/<uuid:id>/comment/edit', api.editComment, name='editComment'),
    path('profile/<uuid:id>/post/delete', api.deletePost, name='deletePost'),
    path('profile/<uuid:id>/post/edit', api.editPost, name='editPost'),
    path('createPost/', api.createPost, name='createPost'),
    path('trends/', api.getTrends, name='getTrends')
]

