from django.db import models
from django.contrib.auth.models import AbstractUser

ARTICLE_STATUS = (
        ('draft', 'Draft'),
        ('inProgress', "In Progress"), 
        ('published', "Published")
    )


class UserProfile(AbstractUser):
    pass

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, default="")
    wordCount = models.IntegerField()
    twitterPost = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, 
        choices=ARTICLE_STATUS,
        default='draft',
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
