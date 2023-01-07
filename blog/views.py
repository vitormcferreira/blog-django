from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

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

        user_id = self.request.user.id

        context['likes'] = models.Interaction.objects.filter(
            post=post, value=models.Interaction.LIKE)
        context['liked'] = context['likes'].filter(user_id=user_id).exists()

        context['dislikes'] = models.Interaction.objects.filter(
            post=post, value=models.Interaction.DISLIKE)
        context['disliked'] = context['dislikes'].filter(
            user_id=user_id).exists()

        context['comment_form'] = forms.CommentForm(initial={'post': post})

        comments = models.Post.objects.filter(parent=post)

        for comment in comments:
            comment.likes = models.Interaction.objects.filter(
                post=comment, value=models.Interaction.LIKE)
            comment.liked = comment.likes.filter(user_id=user_id).exists()

            comment.dislikes = models.Interaction.objects.filter(
                post=comment, value=models.Interaction.DISLIKE)
            comment.disliked = comment.dislikes.filter(
                user_id=user_id).exists()

        context["comments"] = comments

        return context


class CommentViewMixin:
    model = models.Post


class CommentCreateView(
    CommentViewMixin,
    generic.CreateView
):
    http_method_names = ['post']
    form_class = forms.CommentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)

        parent_id = self.kwargs['post_id']

        # se o usuário não estiver autenticado o comentário é feito sem
        # author (NULL)
        if self.request.user.is_authenticated:
            self.object.author = self.request.user

        self.object.parent_id = parent_id

        self.object.save()

        return redirect(reverse_lazy('blog:post_detail', args=[parent_id]))


class InteractionView(LoginRequiredMixin, generic.View):
    def post(self, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['pk'])
        type_ = self.request.GET.get('type')

        match type_:
            case 'like':
                self._like(post)
            case 'dislike':
                self._dislike(post)

        return JsonResponse(data={}, status=201)

    def _like(self, post):
        self._try_interact(post, models.Interaction.LIKE)

    def _dislike(self, post):
        self._try_interact(post, models.Interaction.DISLIKE)

    def _try_interact(self, post, value):
        try:
            self._set_interaction(post, value)
        except:
            self._create_interaction(post, value)

    def _set_interaction(self, post, value):
        interaction = models.Interaction.objects.get(
            post=post, user=self.request.user)

        already_interacted = interaction.value == str(value)

        if already_interacted:
            interaction.delete()
            return

        interaction.value = value
        interaction.save()

    def _create_interaction(self, post, value):
        models.Interaction.objects.create(
            post=post, user=self.request.user, value=value)
