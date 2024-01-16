from django import forms
from . import models
from .models import Comment

class CreateBlog(forms.ModelForm):
    class Meta:
        model = models.Blog
        fields = ["title","body","slug","thumb"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }