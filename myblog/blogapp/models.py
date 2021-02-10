from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField('date published')
    body = models.TextField()
    writer = models.CharField(max_length=100, default="anonymous")

    choice = (('da','daily'),
    ('me','memo'),
    ('wi','wish'),
    ('th','think'))
    tag = models.CharField(max_length=2, choices=choice, default='da')

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:20]+'...'

class Photo(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
