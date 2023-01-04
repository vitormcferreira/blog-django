from django.contrib.auth.models import User
from django.db import models


class Likeable(models.Model):
    likes = models.IntegerField(default=0, auto_created=True)
    dislikes = models.IntegerField(default=0, auto_created=True)

    class Meta:
        abstract = True


class HasAuthor(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class Post(Likeable, HasAuthor):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    text = models.TextField()


class Comment(Likeable, HasAuthor):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
