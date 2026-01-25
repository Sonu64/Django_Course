from django.contrib import admin
from app.models import UserProfile, Article
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "wordCount", "status", "createdAt", "updatedAt") # we avoid to show the content field here
    list_filter = ("status",)
    search_fields = ("title", "content",) # We can still search by the content, no matter it is displayed or not
    date_hierarchy = "createdAt"
    ordering = ("createdAt",)
    readonly_fields = ("wordCount", "createdAt", "updatedAt",)
    

admin.site.register(UserProfile)
admin.site.register(Article, ArticleAdmin)


