from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm

from .models import Group, Post

User = get_user_model()


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = user_obj.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user_obj': user_obj,
        'page_obj': page_obj
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    posts_count = post.author.posts.count()
    context = {
        'post': post,
        'posts_count': posts_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(data=request.POST)

    if request.method != 'POST':
        form = PostForm()
        return render(request, 'posts/post_create.html', {'form': form})

    if not form.is_valid():
        return render(request, 'posts/post_create.html', {'form': form})

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author)


@login_required
def post_edit(request, post_id):
    is_edit = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=is_edit)

    if is_edit.author != request.user:
        return redirect('posts:post_detail', post_id)

    if request.method != 'POST' or not form.is_valid():
        form = PostForm(instance=is_edit)
        return render(
            request, 'posts/post_create.html',
            {
                'form': form,
                'post_id': post_id,
                'is_edit': is_edit
            }
        )

    form.save()
    return redirect('posts:post_detail', post_id)
