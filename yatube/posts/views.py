from django.shortcuts import get_object_or_404, render

from .models import Group, Post


def index(request):
    limit = 10
    posts = Post.objects.all()[:limit]
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    limit = 10
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:limit]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
