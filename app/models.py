from django.db import models
from django.contrib.auth.models import AbstractUser
from app.managers import CustomUserManager
from django.conf import settings
import re
from django.utils.translation import gettext_lazy as _


ARTICLE_STATUS = (
        ('draft', 'Draft'),
        ('inProgress', "In Progress"), 
        ('published', "Published")
    )


class User(AbstractUser):
    email = models.EmailField(_("Email Address"), unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email" # This line is VERY IMPORTANT !! It changes the default username field to email. So now admins can login via email and ONLY email in the admin panel. Earlier only-email login was not possible for admins. It only worked for normal users created via allauth signups.
    
    # In your User model, you have a field called email. By setting USERNAME_FIELD = "email", you are telling Django: "Hey, whenever you're looking for the unique identifier to log someone in, don't look for a column named 'username'. Look for the column named 'email' instead. Username is the default field Django uses to identify users --> Now it will use E-Mail.
    REQUIRED_FIELDS = [] # username is not required anymore, only email and password are required. But username is still a field in the model, just not required. Also if you wanna get via username, you have to look via email now. As specified above.
    
    # GETTER METHODS #
    
    # Get total number of articles created by this user #
    @property
    def article_count(self):
        return self.articles.count()
    
    # Get total number of Words written by this user across all articles #
    @property
    def total_word_count(self):
        # We explicitly name the result 'total'
        data = self.articles.aggregate(total=models.Sum('wordCount'))
        return data['total'] or 0
    
    

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
