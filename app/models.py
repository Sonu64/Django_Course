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
    USERNAME_FIELD = "email" 
    
    # By default, Django's "lock" is configured to accept a "Username" key. By setting USERNAME_FIELD = "email", you are re-keying the lock.You are changing the Authentication key from Username to E-mail !!
    
    # This line is VERY IMPORTANT !! It changes the authentication key. So now admins can login via email and ONLY email in the admin panel. Earlier only-email login was not possible for admins. It only worked for normal users created via allauth signups. Currently the auth key is only the E-Mail.
    
#     Here is exactly what’s happening: even though your models.py doesn't have the "magic" code (to automatically extract username from the email) yet, Django Allauth has a built-in "Username Generator." ### The Mystery Solved
# When you sign up using Allauth with ACCOUNT_AUTHENTICATION_METHOD = "email", Allauth looks at your database and sees that the username column still exists (thanks to AbstractUser). Because it doesn't want to leave that field empty (which can crash certain Django features), it automatically:
# Takes your email: dr.smith@clinic.com.
# Strips the domain: dr.smith.
# Cleans it: Removes illegal characters.
# Saves it into the username column.
# So, when you call {{ user.username }} in your navbar, you are seeing the "cached" version of that extraction that Allauth performed the moment you clicked "Sign Up."

# The "Gotcha" (Why you still need the code)
# While Allauth is doing this for you during Sign Up, it won't happen if:

# You create a user via the Django Admin panel.

# You create a user via the Python Shell (User.objects.create_user).

# You update your email later (the username will stay stuck as the old one).

# Notepad Summary: Allauth Magic
# The Ghost in the Machine: Allauth automatically populates the username field from the email prefix during the signup process.

# Storage: This value is physically stored in your DB, which is why {{ user.username }} works in the navbar.

# Consistency: To ensure this happens everywhere (Admin, Shell, Updates), you should still add that save() method logic we discussed in models.py.

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
