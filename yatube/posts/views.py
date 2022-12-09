from django.shortcuts import get_object_or_404, render

from .models import Group, Post


def index(request):
    title = 'Yatube'
    posts = Post.objects.order_by('-pub_date')[:20]
    context = {
        'posts': posts,
        'title': title
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    title = Group.objects.filter(slug=slug)[0]
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
        'title': title
    }
    return render(request, 'posts/group_list.html', context)
