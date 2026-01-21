# from django.shortcuts import render
from django.http import HttpResponse 
from app.models import Article
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

# Create your views here.

class ArticleListView(ListView):
    template = 'app/home.html'
    model = Article
    context_object_name = "articles"


class ArticleCreateView(CreateView):
    template_name = 'app/create_article.html'
    model = Article
    fields = ["title", "content", "status", "wordCount", "twitterPost"]
    success_url = reverse_lazy('home')
    
    
class ArticleUpdateView(UpdateView):
    template_name = 'app/update_article.html'
    model = Article
    fields = ["title", "content", "status", "wordCount", "twitterPost"]
    success_url = reverse_lazy('home')
    context_object_name = "article"
    

class ArticleDeleteView(DeleteView):
    template_name = 'app/delete_article.html' # id here, just contains something like 
    # do you want to delete {{ article.title }} ?
    model = Article
    success_url = reverse_lazy('home')
    context_object_name = 'article' # this contains the deleted row 
    
    
    



