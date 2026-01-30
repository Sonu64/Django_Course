from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import re

ARTICLE_STATUS = (
        ('draft', 'Draft'),
        ('inProgress', "In Progress"), 
        ('published', "Published")
    )


class User(AbstractUser):
    pass

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, default="")
    wordCount = models.IntegerField(blank=True, default="")
    twitterPost = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, 
        choices=ARTICLE_STATUS,
        default='draft',
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,related_name='articles', on_delete=models.CASCADE) # Creates a creator_ID field in the Articles table
    # User.articles will give all articles related to that user, if User is a row from User table.
    ##### Modified DB models --> Run a migration !!
    ### ONE OFF VALUE OF CURRENT SUPERUSER given during makemigrations. This makes all prev articles with no value of creator.id to use that one off value.
    
    def save(self, *args, **kwargs):
        text = re.sub(r"<[^>]*", "", self.content).replace("&nbsp;", " ")
        self.wordCount = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
