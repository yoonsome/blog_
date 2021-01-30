from django.shortcuts import render

# Create your views here.
# 각각의 html 페이지들을 view 함수 연결함
def blog(request):
    return render(request, 'blog.html')

def home(request):
    blogs = Blog.obje
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def post_ex(request):
    return render(request, 'post_ex.html')

def post(request):
    return render(request, 'post.html')

def signup(request):
    return render(request, 'signup.html')