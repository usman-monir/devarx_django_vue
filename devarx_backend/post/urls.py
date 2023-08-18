from django.urls import path
from . import api

urlpatterns = [
    path('', api.allPosts, name='allPosts'),
    path('profile/<uuid:id>/', api.getUserPosts, name='getUserPosts'),
    path('profile/<uuid:id>/likePost/', api.likePost, name='likePost'),
    path('profile/<uuid:id>/dislikePost/', api.dislikePost, name='dislikePost'),
    path('profile/<uuid:id>/comment/', api.comment, name='comment'),
    path('createPost/', api.createPost, name='createPost')
]

