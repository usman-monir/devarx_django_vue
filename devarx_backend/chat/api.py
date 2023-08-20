from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Conversation, ConversationMessage
from account.models import User
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
def allConversations(request):
    conversations = Conversation.objects.filter(users__in=[request.user])
    conversations = ConversationSerializer(conversations, many=True)
    return JsonResponse({'conversations': conversations.data})


@api_view(['POST'])
def StartOrCreateChat(request):
    userId = request.data.get('userId')
    user = User.objects.get(pk=userId)
    conversations = Conversation.objects.filter(users__in=[request.user])
    conversations = conversations.filter(users__in=[user])
    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user,request.user)
        conversation.save()

    conversation = ConversationDetailSerializer(conversation)
    return JsonResponse({'conversation': conversation.data})


@api_view(['POST'])
def fetchMessages(request, conversationId):
    conversation = Conversation.objects.get(pk=conversationId)
    conversation = ConversationDetailSerializer(conversation)
    return JsonResponse({'activeConversation': conversation.data})


@api_view(['POST'])
def sendMessage(request, conversationId):
    messageBody = request.data.get('messageBody')
    sent_to = request.data.get('sent_to')
    sent_to = User.objects.get(pk=sent_to)

    conversation = Conversation.objects.get(pk=conversationId)
    if conversation:
        message = ConversationMessage.objects.create(conversations=conversation, body=messageBody, sent_by=request.user, sent_to=sent_to)
        message = ConversationMessageSerializer(message)
        return JsonResponse({'message': message.data })
    return JsonResponse({'message': {} })


@api_view(['POST'])
def deleteMessage(request, conversationId):
    messageId = request.data.get('messageId')

    conversation = Conversation.objects.get(pk=conversationId)
    if conversation:
        conversation.messages.get(id=messageId).delete()
        messages = ConversationMessageSerializer(conversation.messages.all(), many=True)
        return JsonResponse({'messages': messages.data })
    return JsonResponse({'messages': {} })


@api_view(['POST'])
def editMessage(request, conversationId):
    messageId = request.data.get('messageId')
    messageBody = request.data.get('messageBody')

    conversation = Conversation.objects.get(pk=conversationId)
    if conversation:
        conversation.messages.filter(id=messageId).update(body=messageBody)
        messages = ConversationMessageSerializer(conversation.messages.all(), many=True)
        return JsonResponse({'messages': messages.data })
    return JsonResponse({'messages': {} })

