from rest_framework import serializers
from .models import User, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email','friends')


class RequestsSerializer(serializers.ModelSerializer):
    send_by = UserSerializer(read_only=True)
    send_to = UserSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ('id', 'send_by', 'send_to',)
