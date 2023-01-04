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
]
