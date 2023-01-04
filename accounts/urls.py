from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path("logout/", auth_views.logout_then_login, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register')
]
