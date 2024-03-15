from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Post, Category


def get_posts():
    return Post.objects.select_related().filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    template = "blog/index.html"
    post_list = (
        get_posts()
        .order_by("-pub_date")[:5]
    )
    context = {"post_list": post_list}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    post_list = get_posts().filter(category=category)
    context = {"category": category, "post_list": post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = "blog/detail.html"
    post = get_object_or_404(
        get_posts().filter(pk=post_id)
    )
    context = {"post": post}
    return render(request, template, context)
