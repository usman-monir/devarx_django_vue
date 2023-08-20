from django.db import models
from account.models import User
import uuid
from django.utils.timesince import timesince

# Create your models here.


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def created_at_formatted(self):
        return timesince(self.created_at)

    def modified_at_formatted(self):
        return timesince(self.modified_at)


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    conversations = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)

    def __str__(self) -> str:
        return f'{self.sent_by.name} -> {self.body} -> {self.sent_to.name}'

    def created_at_formatted(self):
        return timesince(self.created_at)
