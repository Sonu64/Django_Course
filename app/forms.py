from django import forms 
from app.models import Article


class CreateArticleForm(forms.Form):
    class Meta:
        model = Article
        fields = ("title", "content", "wordCount", "twitterPost", "status")