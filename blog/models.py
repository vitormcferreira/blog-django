from django.contrib.auth.models import User
from django.db import models


class Interaction(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    LIKE = 'LK', 'like'
    DISLIKE = 'DL', 'dislike'

    value = models.CharField(
        choices=[LIKE, DISLIKE], max_length=2)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255, null=True)
    abstract = models.TextField(null=True)
    text = models.TextField()

    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    interactions = models.ManyToManyField(
        User, through=Interaction, related_name='interacted_posts')
