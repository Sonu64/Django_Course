# from django.shortcuts import render
from django.http import HttpResponse 
from app.models import Article
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView


# Create your views here.

def home(req):
    allArticles = Article.objects.all() # Using Django ORM for the 1st time ⏰
    return render(req, "app/home.html", {"articles":allArticles})



# Function Based View
# def createArticle(req):
#     if req.method == 'POST':
#         form = CreateArticleForm(req.POST)
#         if form.is_valid():
#             formData = form.cleaned_data
#             newArticle = Article(
#                 title = formData['title'],
#                 status = formData['status'],
#                 content = formData['content'],
#                 wordCount = formData['wordCount'],
#                 twitterPost = formData['twitterPost']
#             )
#             newArticle.save() 
#             return redirect('home')       
        
#     elif req.method == 'GET':
#         form = CreateArticleForm()
        
#     return render(req, 'app/create_article.html', {'form':form})


class ArticleCreateView(CreateView):
    template_name = 'app/create_article.html'
    model = Article
    fields = ["title", "content", "status", "wordCount", "twitterPost"]
    success_url = reverse_lazy('home')
    
    
    



