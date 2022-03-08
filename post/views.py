from django.shortcuts import render, get_object_or_404, redirect

from home.models import Setting

from .forms import CommentForm
from .models import Category, Post, Tag

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
categories = Category.objects.all()
tags = Tag.objects.all()
settings = Setting.objects.first()

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            comment = form.save()
            comment.post = post
            comment.ip = request.META.get('REMOTE_ADDR')
            url = request.META.get('HTTP_REFERER')
            comment.save()
            messages.success(request, 'Comment added.')
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, 'Message could not be sent.')

    context = {
        'post': post,
        'form': form,
        'settings': settings,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'blog/detail.html', context)


@login_required()
def delete_post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    try:
        post.delete()
        messages.success(request, "Post deleted!")
    except:
        messages.error(request, "Post not deleted!")

    return redirect('home:home')


def category(request, id, slug):
    category = get_object_or_404(Category, slug=slug)
    context = {
        'category': category,
        'posts': Post.objects.filter(category_id=id),
        'settings': settings,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'blog/category.html', context)


def tag(request, id, slug):
    tag = get_object_or_404(Tag, slug=slug)
    context = {
        'tag': tag,
        'posts': Post.objects.filter(tags=tag),
        'settings': settings,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'blog/tag.html', context)
