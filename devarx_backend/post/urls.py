from django.urls import path
from . import api

urlpatterns = [
    path('', api.allPosts, name='allPosts'),
    path('profile/<uuid:id>/', api.getUserPosts, name='getUserPosts'),
    path('createPost/', api.createPost, name='createPost')
]

