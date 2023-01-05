from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST

from . import forms, models


class PostViewMixin:
    model = models.Post
    fields = ['title', 'abstract', 'text']


class SuccessUrlToPostDetailMixin:
    def get_success_url(self) -> str:
        return reverse_lazy('blog:post_detail', args=[self.object.pk])


class FilterQuerySetByAuthorMixin:
    def get_queryset(self):
        qs: QuerySet = super().get_queryset()

        qs = qs.filter(author=self.request.user)

        return qs


class PostCreateView(
    PostViewMixin,
    LoginRequiredMixin,
    FilterQuerySetByAuthorMixin,
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
    FilterQuerySetByAuthorMixin,
    SuccessUrlToPostDetailMixin,
    generic.UpdateView
):
    pass


class PostDeleteView(
    PostViewMixin,
    LoginRequiredMixin,
    FilterQuerySetByAuthorMixin,
    generic.DeleteView
):
    success_url = reverse_lazy('blog:home')


class PostDetailView(PostViewMixin, generic.DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object

        context['comment_form'] = forms.CommentForm(initial={'post': post})
        context["comments"] = models.Comment.objects.filter(post=post)

        return context


class CommentViewMixin:
    model = models.Comment


class CommentCreateView(
    CommentViewMixin,
    generic.CreateView
):
    http_method_names = ['post']
    form_class = forms.CommentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        post_id = self.kwargs['post_id']

        # se o usuário não estiver autenticado o comentário é feito sem
        # author (NULL)
        if self.request.user.is_authenticated:
            self.object.author = self.request.user

        self.object.post_id = post_id

        self.object.save()

        return redirect(reverse_lazy('blog:post_detail', args=[post_id]))


@require_POST
@login_required
def post_increment_like_view(_, pk):
    models.Post.objects.filter(pk=pk).update(likes=F('likes') + 1)
    return HttpResponse(status=201)


@require_POST
@login_required
def post_increment_dislike_view(_, pk):
    models.Post.objects.filter(pk=pk).update(dislikes=F('dislikes') + 1)
    return HttpResponse(status=201)


@require_POST
@login_required
def comment_increment_like_view(_, pk):
    models.Comment.objects.filter(pk=pk).update(likes=F('likes') + 1)
    return HttpResponse(status=201)


@require_POST
@login_required
def comment_increment_dislike_view(_, pk):
    models.Comment.objects.filter(pk=pk).update(dislikes=F('dislikes') + 1)
    return HttpResponse(status=201)
