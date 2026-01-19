from django import forms 
from app.models import ARTICLE_STATUS # Already imported Article Status here, not required to define below.


class CreateArticleForm(forms.Form):
    title = forms.CharField(max_length=100)
    status = forms.ChoiceField(choices=ARTICLE_STATUS)
    content = forms.CharField(widget = forms.Textarea)
    wordCount = forms.IntegerField()
    twitterPost = forms.CharField(widget=forms.Textarea, required=False)