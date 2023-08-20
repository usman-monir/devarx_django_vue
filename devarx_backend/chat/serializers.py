from .models import Conversation, ConversationMessage
from rest_framework import serializers
from account.serializers import UserSerializer

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'created_at_formatted', 'modified_at_formatted',)


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_by = UserSerializer(read_only=True)
    sent_to = UserSerializer(read_only=True)
    class Meta:
        model = ConversationMessage
        fields = ('id', 'body', 'created_at_formatted', 'sent_by', 'sent_to',)


class ConversationDetailSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    messages = ConversationMessageSerializer(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ('id', 'users', 'messages', 'created_at_formatted', 'modified_at_formatted')

