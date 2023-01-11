from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, Count, QuerySet, When
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


class FilterQuerySetOnlyPostsMixin:
    def get_queryset(self) -> QuerySet[models.Post]:
        # Posts diferem de comentários por não possuírem um parent
        return super().get_queryset().filter(parent__isnull=True)


class PostListView(
    PostViewMixin,
    FilterQuerySetOnlyPostsMixin,
    generic.ListView
):
    template_name = 'blog/home.html'


class PostCreateView(
    PostViewMixin,
    LoginRequiredMixin,
    FilterQuerySetByAuthorMixin,
    SuccessUrlToPostDetailMixin,
    generic.CreateView
):
    def form_valid(self, form):
        self.object = form.save(commit=False)

        self._add_object_author()

        self.object.save()
        return redirect(self.get_success_url())

    def _add_object_author(self):
        self.object.author = self.request.user


class PostUpdateView(
    PostViewMixin,
    LoginRequiredMixin,
    FilterQuerySetByAuthorMixin,
    FilterQuerySetOnlyPostsMixin,
    SuccessUrlToPostDetailMixin,
    generic.UpdateView
):
    pass


class PostDeleteView(
    PostViewMixin,
    LoginRequiredMixin,
    FilterQuerySetByAuthorMixin,
    FilterQuerySetOnlyPostsMixin,
    generic.DeleteView
):
    success_url = reverse_lazy('blog:home')


class PostDetailView(
    PostViewMixin,
    FilterQuerySetOnlyPostsMixin,
    generic.DetailView
):
    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            qs = self._annotate_liked_post(qs)
            qs = self._annotate_disliked_post(qs)

        return qs

    def _annotate_liked_post(self, qs):
        return qs.annotate(liked=self._has_interacted(
            models.Interaction.LIKE))

    def _annotate_disliked_post(self, qs):
        return qs.annotate(disliked=self._has_interacted(
            models.Interaction.DISLIKE))

    def _has_interacted(self, value):
        return Count(Case(
            When(interaction__user=self.request.user,
                 interaction__value=value,
                 then=True))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object
        user_id = self.request.user.id

        self._add_comment_form(context)

        # TODO: adicionar campos liked e disliked dos comments em get_queryset
        comments = post.comments.all()
        for comment in comments:
            comment.liked = comment.likes.filter(id=user_id).exists()
            comment.disliked = comment.dislikes.filter(
                id=user_id).exists()

        context['comments'] = comments

        return context

    def _add_comment_form(self, context):
        context['comment_form'] = forms.CommentForm(
            initial={'post': self.object})


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

        # se o usuário não estiver autenticado o comentário é feito como
        # anônimo (author = NULL)
        self._set_object_author_if_authenticated()
        self._set_object_parent()

        self.object.save()
        return redirect(reverse_lazy(
            'blog:post_detail', args=[self.object.parent_id]))

    def _set_object_author_if_authenticated(self):
        if self.request.user.is_authenticated:
            self.object.author = self.request.user

    def _set_object_parent(self):
        self.object.parent_id = self.kwargs['post_id']


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
        self._interact(post, models.Interaction.LIKE)

    def _dislike(self, post):
        self._interact(post, models.Interaction.DISLIKE)

    def _interact(self, post, value):
        try:
            self._try_set_interaction(post, value)
        except:
            self._create_interaction(post, value)

    def _try_set_interaction(self, post, value):
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
