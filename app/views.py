# from django.shortcuts import render
from django.http import HttpResponse 
from app.models import Article
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

# Create your views here.

class ArticleListView(ListView):
    template_name = 'app/home.html'
    model = Article
    context_object_name = "articles"


class ArticleCreateView(CreateView):
    template_name = 'app/create_article.html'
    model = Article
    fields = ["title", "content", "status", "wordCount", "twitterPost"]
    success_url = reverse_lazy('home')
    
    
    
class ArticleUpdateView(UpdateView):
    # Primary Key = ID, fetched from Route, automatically by Django Magic !
    # UpdateView fetches the article with that ID, pre-fills the form with its values
    # And stores this fetched article in the context_object_name
    template_name = 'app/update_article.html'
    model = Article
    fields = ["title", "content", "status", "wordCount", "twitterPost"]
    success_url = reverse_lazy('home')
    context_object_name = "article" # this contains the row to be updated
    

class ArticleDeleteView(DeleteView):
    # Primary Key = ID, fetched from Route, automatically by Django Magic !
    # DeleteView deletes the article with that id if success_url hit.
    # Else it just stores the article in an object, and not delete it if we go back.
    template_name = 'app/delete_article.html'
    model = Article
    success_url = reverse_lazy('home')
    context_object_name = 'article' # this contains the deleted row 
    
    
    



