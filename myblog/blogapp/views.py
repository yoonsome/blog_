from django.shortcuts import render, redirect
from .models import Blog
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
# 각각의 html 페이지들을 view 함수 연결함
def blog(request):
    return render(request, 'blog.html')


def home(request):
    blogs=Blog.objects
    return render(request, 'home.html', {'blogs':blogs})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(username = request.POST["username"], password = request.POST["password1"])
            auth.login(request,user)
            return redirect('home')
        return render(request, 'blog.html')
    else: return render(request,'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('blog')


def post_ex(request):
    return render(request, 'post_ex.html')

def post(request):
    return render(request, 'post.html')