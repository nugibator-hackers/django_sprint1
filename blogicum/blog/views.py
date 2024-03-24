from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView, CreateView, ListView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeletionMixin
from django.views import View

from blog.models import Post, Category, User, Comment
from blog.forms import PostForm, CommentForm

SLICE_POSTS = 10


def get_posts():
    return Post.objects.select_related().filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )

def get_publish_posts():
    return get_posts().filter(is_published=True,
                              category__is_published=True,)


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = SLICE_POSTS

    def get_queryset(self):
        return get_publish_posts()

class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = SLICE_POSTS
    category = None

    def get_queryset(self):
        self.category = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        return get_publish_posts().filter(category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context
    

class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = SLICE_POSTS
    author = None

    def get_queryset(self):

        self.author = get_object_or_404(User, username = self.kwargs['username'])
        if self.author == self.request.user:
            return get_posts().filter(author = self.author)
        return get_publish_posts().filter(author = self.author)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs['username']
        )
        return context
    
class ProfileViewEdit(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/user.html'
    fields = ('username', 'first_name', 'last_name', 'email')

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

class PostEditView(UpdateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', self.get_object().pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.object.pk,))

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', args=(self.object.author,))


class PostDeleteView(DeletionMixin, PostEditView):
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', self.get_object().pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', args=(self.request.user.username,))

class CommentView(LoginRequiredMixin, View):
    object = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        form.instance.object = self.object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=(self.object.post_id,))
    
    
class CommentUpdateView(CommentView, UpdateView):
    form_class = CommentForm

class CommentDeleteView(CommentView, DeleteView):
    pass