from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from . import models


class PostViewMixin:
    model = models.Post
    fields = ['title', 'abstract', 'text']


class SuccessUrlToPostDetailMixin:
    def get_success_url(self) -> str:
        return reverse_lazy('blog:post_detail', args=[self.object.pk])


class PostCreateView(
    PostViewMixin,
    LoginRequiredMixin,
    SuccessUrlToPostDetailMixin,
    generic.CreateView
):
    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.author = self.request.user
        self.object.save()

        return redirect(self.get_success_url())


class PostUpdateView(
    PostViewMixin,
    LoginRequiredMixin,
    SuccessUrlToPostDetailMixin,
    generic.UpdateView
):
    pass


class PostDeleteView(
    PostViewMixin,
    LoginRequiredMixin,
    generic.DeleteView
):
    success_url = reverse_lazy('blog:home')


class PostDetailView(PostViewMixin, generic.DetailView):
    pass
