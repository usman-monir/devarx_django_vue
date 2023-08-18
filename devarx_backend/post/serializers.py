from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_at_formatted', 'created_by')

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    likes = UserSerializer(many=True)
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_at_formatted', 'created_by', 'likes', 'comments',)
