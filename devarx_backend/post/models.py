import uuid
from django.db import models
from django.utils.timesince import timesince
from account.models import User


# Create your models here.

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_by',)

    def __str__(self) -> str:
        return self.body

    def created_at_formatted(self):
        return timesince(self.created_at)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    attachments = models.ManyToManyField(PostAttachment, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    comments = models.ManyToManyField(Comment, related_name='post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)


    class Meta:
        ordering = ('-created_at',)


    def __str__(self) -> str:
        return self.body

    def created_at_formatted(self):
        return timesince(self.created_at)
