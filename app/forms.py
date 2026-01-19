from django import forms 


class CreateArticleForm(forms.Form):
    
    ARTICLE_STATUS = (
        ('draft', 'Draft'),
        ('inProgress', "In Progress"), 
        ('published', "Published")
    )
    
    title = forms.CharField(max_length=100)
    status = forms.ChoiceField(choices=ARTICLE_STATUS)
    content = forms.CharField(widget = forms.Textarea)
    wordCount = forms.IntegerField()
    twitterPost = forms.CharField(widget=forms.Textarea, required=False)