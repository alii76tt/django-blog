from django.contrib import messages
from django.shortcuts import render


from .forms import ContactForm
from .models import Setting, About
from post.models import Post, Category, Tag
from django.http.response import HttpResponseRedirect

# Create your views here.
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

categories = Category.objects.all()
tags = Tag.objects.all()
settings = Setting.objects.first()


def index(request):
    post_list = Post.objects.all()

    paginator = Paginator(post_list, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        posts = post_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)).distinct()

    context = {
        'post_list': post_list,
        'posts': posts,
        'settings': settings,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'home/index.html', context)


def about(request):
    context = {
        'about': About.objects.first(),
        'settings': settings,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'home/about.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            contact = form.save()
            contact.ip = request.META.get('REMOTE_ADDR')
            url = request.META.get('HTTP_REFERER')
            contact.save()
            messages.success(request, 'Message sent.')
            return HttpResponseRedirect(url)
        else:
            messages.warning(request, 'Message could not be sent.')

    context = {
        'form': form,
        'settings': settings,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'home/contact.html', context)
