from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, blank=False)
    name = models.CharField(max_length=255, default='', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_avatar(self):
        if self.avatar:
            return 'http://127.0.0.1:8000' + self.avatar.url
        else:
            return 'https://thumbs.dreamstime.com/b/default-avatar-profile-image-vector-social-media-user-icon-potrait-182347582.jpg'


class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    send_by = models.ForeignKey(User, related_name='friend_requests_sendby', on_delete=models.CASCADE)
    send_to = models.ForeignKey(User, related_name='friend_requests_sendto', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.send_by.email + ' -> ' + self.send_to.email
