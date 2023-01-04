from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class IsNotAuthenticatedUser:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:home')

        return super().dispatch(request, *args, **kwargs)


class LoginView(IsNotAuthenticatedUser, auth_views.LoginView):
    next_page = 'blog:home'


class RegisterView(IsNotAuthenticatedUser, CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/register.html'
