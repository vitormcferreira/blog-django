from django.urls import path
from django.views import generic

from . import models, views

app_name = 'blog'

urlpatterns = [
    path('', generic.ListView.as_view(
        model=models.Post,
        template_name='blog/home.html',
    ), name='home'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_update/<pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post_detail/<pk>/', views.PostDetailView.as_view(), name='post_detail'),

    path('comment_create/<post_id>/',
         views.CommentCreateView.as_view(), name='comment_create'),

    # Requisições feitas com Ajax
    path('post_increment_like/<pk>/', views.post_increment_like_view,
         name='post_increment_like'),
    path('post_increment_dislike/<pk>/', views.post_increment_dislike_view,
         name='post_increment_dislike'),
    path('comment_increment_like/<pk>/', views.comment_increment_like_view,
         name='comment_increment_like'),
    path('comment_increment_dislike/<pk>/', views.comment_increment_dislike_view,
         name='comment_increment_dislike'),
]
