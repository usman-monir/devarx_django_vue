from django.urls import path
from . import api

urlpatterns = [
    path('', api.allConversations, name='allConversations'),
    path('<uuid:conversationId>/', api.fetchMessages, name='fetchMessages'),
    path('<uuid:conversationId>/sendMessage/', api.sendMessage, name='sendMessage'),
    path('<uuid:conversationId>/deleteMessage/', api.deleteMessage, name='deleteMessage'),
    path('<uuid:conversationId>/editMessage/', api.editMessage, name='editMessage'),
    path('initialize/', api.StartOrCreateChat, name='startOrCreateChat')
]

