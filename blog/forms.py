from django.forms.models import ModelForm

from . import models


class CommentForm(ModelForm):
    class Meta:
        model = models.Post
        fields = ['text']
