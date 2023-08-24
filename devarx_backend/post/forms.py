from django import forms
from .models import Post, PostAttachment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class PostAttachmentForm(forms.ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)
