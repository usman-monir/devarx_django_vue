from django.urls import path
from . import api

urlpatterns = [
    path('', api.all_posts, name='all_posts'),
    path('create_post/', api.create_post, name='createPost')
]

