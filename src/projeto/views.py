from typing import Optional
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        base_template = "base_authenticated.html"
        posts = Post.objects.all().filter(group__isnull=True)
    else:
        base_template = "base.html"
        posts = Post.objects.all().filter(is_login_required=0, group__isnull=True)

    context = {
        'base_template': base_template,
        'posts': posts
    }

    return render(request, 'index.html', context)

@login_required(login_url='/login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            newPost = Post(
                title=form.cleaned_data['title'], 
                content=form.cleaned_data['content'],
                image=form.cleaned_data['image'],
                is_login_required=0,
                group=form.cleaned_data['group'],
                created_by=request.user)
            
            newPost.save()
            return redirect('/')
        
    postForm = PostForm()
    postForm.fields['group'].choices = [('', 'Nenhum')]
    postForm.fields['group'].choices += [(c.id, c.name) for c in request.user.groups.all()]
    context = {
        'form': postForm
    }

    return render(request, 'posts/create.html', context)
    

@login_required(login_url='/login')
def groups(request):
    context = {
        'groups': request.user.groups.all()
    }

    return render(request, 'groups.html', context)


@login_required(login_url='/login')
def group(request, id):
    group = Group.objects.all().filter(id=id).first()
    posts = Post.objects.all().filter(group__id=id)

    context = {
        'group': group,
        'posts': posts
    }

    return render(request, 'group.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['txbUsername'], password=request.POST['txbPassword'])

        if user is not None:
            auth_login(request, user)
            return redirect('/')

    context = {}
    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('/')