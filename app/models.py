from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import re
from django.utils.translation import gettext_lazy as _


ARTICLE_STATUS = (
        ('draft', 'Draft'),
        ('inProgress', "In Progress"), 
        ('published', "Published")
    )


class User(AbstractUser):
    pass

class Article(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    content = models.TextField(_("Content"), blank=True, default="")
    wordCount = models.IntegerField(_("Word Count"), blank=True, default=0)
    twitterPost = models.TextField(_("Twitter Post"), blank=True, default="")
    status = models.CharField(
        _("Status"),
        max_length=20, 
        choices=ARTICLE_STATUS,
        default='draft',
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,related_name='articles', on_delete=models.CASCADE, verbose_name=_("Creator")) # Creates a creator_ID field in the Articles table
    # User.articles will give all articles related to that user, if User is a row from User table.
    ##### Modified DB models --> Run a migration !!
    ### ONE OFF VALUE OF CURRENT SUPERUSER given during makemigrations. This makes all prev articles with no value of creator.id to use that one off value.
    
    def save(self, *args, **kwargs):
        text = re.sub(r"<[^>]*", "", self.content).replace("&nbsp;", " ")
        self.wordCount = len(re.findall(r"\b\w+\b", text))
        super().save(*args, **kwargs)
