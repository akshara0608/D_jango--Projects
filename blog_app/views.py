from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .models import Post
from .forms import PostForm

# Home Page

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog_app/home.html', {'posts': posts})

# Signup Page

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')

    return render(request, 'blog_app/signup.html')

# Create Post

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'blog_app/create_post.html', {'form': form})

# Post Detail

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog_app/post_detail.html', {'post': post})

# Logout

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'blog_app/profile.html')