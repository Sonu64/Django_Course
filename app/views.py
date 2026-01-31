# from django.shortcuts import render
from app.models import Article
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from typing import Any

# Create your views here.

class ArticleListView(LoginRequiredMixin, ListView):
    template_name = 'app/home.html'
    model = Article
    context_object_name = "articles"
    
    def get_queryset(self):
        return Article.objects.filter(creator=self.request.user).order_by('-createdAt')
        # self.get_object() won't work because this URL does not take a URL Path param, like UpdateView and DeleteView does. get_object() simply find the model row associated with that ID. But here self.request.user works because it points to the user object sending the request.


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app/create_article.html'
    model = Article
    fields = ["title", "content", "status", "twitterPost"]
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)
        # In Python, super() (the function) returns an object that allows you to call any method on the parent (following the MRO, since multiple inheritance is possible in Python !), including __init__, form_valid, or any custom logic.
        # In Java, super is a keyword, but in Python super() is a method 
    
    
    
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Primary Key = ID, fetched from Route, automatically by Django Magic !
    # UpdateView fetches the article with that ID, pre-fills the form with its values
    # And stores this fetched article in the context_object_name
    template_name = 'app/update_article.html'
    model = Article
    fields = ["title", "content", "status", "twitterPost"]
    success_url = reverse_lazy('home')
    context_object_name = "article" # this contains the row to be updated
    
    def test_func(self):
        # 1. Fetch the specific row from the DB
        article = self.get_object() 
        # 2. Comparison Logic
        if self.request.user == article.creator:
            return True
        else:
            return False
        
        # Why not self.creator ? SHORT ANSWER --> Because here self is the ArticleUpdateView obj, not article obj.
        # When you are inside ArticleUpdateView, self refers to the instance of the View class that is currently handling the web request. It has methods like get_object(), but it doesn't automatically inherit the fields of the Article model.

        # self.request: The incoming HTTP request.

        # self.model: A reference to the class Article, not a specific row.

        # self.get_object(): This is the "Search" command that returns the specific Model Instance (the row) you want to edit.
    

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # Primary Key = ID, fetched from Route, automatically by Django Magic !
    # DeleteView deletes the article with that id if success_url hit.
    # Else it just stores the article in an object, and not delete it if we go back.
    template_name = 'app/delete_article.html'
    model = Article
    success_url = reverse_lazy('home')
    context_object_name = 'article' # this contains the deleted row 
    
    def test_func(self):
        # 1. Fetch the specific row from the DB
        article = self.get_object() 
        # 2. Comparison Logic
        if self.request.user == article.creator:
            return True
        else:
            return False


