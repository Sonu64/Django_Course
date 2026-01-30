from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import User, Article
# Register your models here.

# File to control what the Admin will see about the Models.

class CustomUserAdmin(UserAdmin):
    # We can customize the UserAdmin here if needed, for now we will use the default settings, initially used User model given to us by  django.models...jst like class User(User):[...code...] but now we are creating our own CustomUserAdmin inherited from django.contrib.auth.admin.UserAdmin....we could have named UserAdmin(UserAdmin), but we prefixef with Custom just to avoid naming confusions with the default useradmin class -> UserAdmin
    search_fields = ("email",)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "wordCount", "status", "createdAt", "updatedAt",) # we avoid to show the content field here
    list_filter = ("status",)
    search_fields = ("title", "content",) # We can still search by the content, no matter it is displayed or not
    date_hierarchy = "createdAt"
    ordering = ("createdAt",)
    readonly_fields = ("wordCount", "createdAt", "updatedAt",)
    

admin.site.register(User, CustomUserAdmin) # Here User is the default User model we created in models.py - inheriting from Djangos AbstractUser class.
admin.site.register(Article, ArticleAdmin)

### ------- SYNTAX REMINDER FOR ADMIN CUSTOMIZATION -------- ###
# admin.site.register(ModelName, ModelAdminClassName)


