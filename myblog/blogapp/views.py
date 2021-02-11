from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Photo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib import auth
from django.core.paginator import Paginator
from .form import BlogPost
from django.contrib.auth.decorators import login_required

# Create your views here.
# 각각의 html 페이지들을 view 함수 연결함


def blog(request):
    if request.user.is_authenticated:
        return render(request,'home.html')
    else:
        return render(request,'blog.html')

def home(request):
    blogs= Blog.objects
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list,6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    if request.user.is_authenticated:
        return render(request, 'home.html', {'blogs':blogs,'posts':posts, 'user':request.user.username, 'login':'logout'})
    else:
        return render(request, 'home.html', {'blogs':blogs,'posts':posts, 'login':'login'})


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
            return redirect('blog')
        return render(request, 'blog.html')
    else: return render(request,'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('blog')


def post_ex(request):
    return render(request, 'post_ex.html')

@login_required(login_url='login')
def detail(request,blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    print(blog_detail.tag)
    return render(request, 'post_ex.html', {'blog':blog_detail, 'username':request.user.username})

@login_required(login_url='login')
def create(request):
    blog=Blog()
    blog.title = request.POST['title']
    blog.body = request.POST['body']
    blog.pub_date = timezone.datetime.now()
    blog.writer = request.user.username
    blog.tag = request.POST['tag']
    blog.save()
    # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다 
    for img in request.FILES.getlist('imgs'):
        # Photo 객체를 하나 생성한다.
        photo = Photo()
        # 외래키로 현재 생성한 Post의 기본키를 참조한다.
        photo.post = blog
        # imgs로부터 가져온 이미지 파일 하나를 저장한다.
        photo.image = img
        # 데이터베이스에 저장
        photo.save()
    return redirect('/home/'+str(blog.id))

def blogpost(request):
    if request.method == "POST":
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:
        form = BlogPost()
        return render(request, 'post.html', {'form':form})


def delete(request, blog_id):
    post = Blog.objects.get(id=blog_id)
    if request.user.username == post.writer:
        post.delete()
        return redirect('home')
    else:
        return redirect('home')   #작성자와 다를 때 삭제 불가능 OK, 팝업 창 띄우기 못함

def edit(request, blog_id):
    post = Blog.objects.get(id=blog_id)
    if request.user.username == post.writer:
        if request.method == "POST":
            form = BlogPost(request.POST)
            print(">>>>>>",form)
            if form.is_valid():
                print(form.cleaned_data)
                post.title = form.cleaned_data['title']
                post.body = form.cleaned_data['body']
                photo = Photo.objects.filter(post=blog_id)
                photo.delete()
                for img in request.FILES.getlist('imgs'):
                    # Photo 객체를 하나 생성한다.
                    photo = Photo()
                    # 외래키로 현재 생성한 Post의 기본키를 참조한다.
                    photo.post = post
                    # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                    photo.image = img
                    # 데이터베이스에 저장
                    photo.save()
                post.save()
            return redirect('/home/'+str(blog_id))
        else:
            form = BlogPost(instance = post)
            context={
                'form':form,
                'title':post.title,
                'body':post.body,
                'imgs':Photo.objects.filter(post=blog_id)
            }
            return render(request, 'edit_post.html', context)
    else:
        return redirect('home')
