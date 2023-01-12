from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_update/<pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post_detail/<pk>/', views.PostDetailView.as_view(), name='post_detail'),

    path('comment_create/<post_id>/',
         views.CommentCreateView.as_view(), name='comment_create'),
    path('comment_delete/<post_id>/<pk>/',
         views.CommentDeleteView.as_view(), name='comment_delete'),

    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),

    # Requisições feitas com Ajax
    path('interaction/<pk>/', views.InteractionView.as_view(), name='interaction'),
]
