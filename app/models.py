from django.db import models
from django.contrib.auth.models import AbstractUser
import re

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
    
    def save(self, *args, **kwargs):
        text = re.sub(r"<[^>]*", "", self.content).replace("&nbsp;", " ")
        self.wordCount = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
