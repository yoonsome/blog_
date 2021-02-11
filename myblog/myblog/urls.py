"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import blogapp.views
import userapp.views
#이미지 위해 추가
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',blogapp.views.blog, name='blog'),
    path('home/', blogapp.views.home, name='home'),
    path('login/', userapp.views.login, name='login'),
    path('/accounts/',include('allauth.urls')),
    path('post_ex/', blogapp.views.post_ex, name='post_ex'),
    path('create/',blogapp.views.create, name='create'),
    path('signup/', blogapp.views.signup, name='signup'),
    path('logout/', blogapp.views.logout, name='logout'),
    path('post/', blogapp.views.blogpost, name='newblog'),
    path('home/<int:blog_id>',blogapp.views.detail, name='detail'),
    path('home/<int:blog_id>/delete',blogapp.views.delete, name='delete'),
    path('home/<int:blog_id>/edit', blogapp.views.edit, name='edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
