from django import forms
from .models import Blog, Photo

class BlogPost(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','body']