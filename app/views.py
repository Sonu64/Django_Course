# from django.shortcuts import render
from urllib3 import request

from app.models import Article
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
# 1. For ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
# 2. For ProtectedError (The one you're missing)
from django.db.models import ProtectedError
# 3. For IntegrityError and DatabaseError
from django.db import IntegrityError, DatabaseError
from django import http
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
        
        try:
            # 1. Queue the success message
            messages.success(self.request, "Article created successfully!", extra_tags="creation")
            # 2. Attempt the DB Insert
            return super().form_valid(form)
            
        except DatabaseError:
            # 3. DB died? Queue error and stay on form
            messages.error(self.request, "Critical: Database connection lost. Try again.")
            return self.form_invalid(form) 
        
    def form_invalid(self, form):   
        # If we reach here, it means the user input was wrong (e.g. title too long)
        
        # form_invalid is the Security Guard at the front door. He checks the paperwork (the form). If the name is missing or the ID is invalid, he sends the person away immediately. He doesn't call the "Article" (the Database) because the paperwork is already wrong. No Database connection is needed to see that a field is empty!
        
        # It is important to understand that form_invalid is triggered by user input errors, not by database errors. So, we can safely add a message here without worrying about database exceptions, because if the form is invalid, it means we haven't even tried to save to the database yet.
        
        messages.error(self.request, "Error: Please correct the marked fields below.")
        return super().form_invalid(form)
    
    
    
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
        
    def post(self, request, *args, **kwargs):
            """
            Overriding post is the most reliable way to handle messages in DeleteView.
            """
            # Get the article object to be deleted using get_object(), which is provided by the DeleteView and fetches the object based on the URL parameter (like ID).
            
            # When the DeleteView is first "born" to handle a click:

            # self exists (the instance).

            # self.object is technically an attribute the class expects to have, but at the very start of the post method, it hasn't been assigned anything yet (it's essentially a hollow shelf).

            # self.get_object() goes to the warehouse (Database), grabs the specific article, and you then place it on that shelf by saying self.object = ....

            # In Python, every class instance has self, but self.object is a specific convention used by Django's Generic Views (like DetailView, UpdateView, and DeleteView).

            # 1. self = The Identity
            # Every object in Python uses self to refer to itself. It’s like a person saying "I" or "Me."

            # self.name = "My name"

            # self.delete() = "I am deleting myself"

            # 2. self.object = The Target
            # In the specific case of Django’s SingleObjectMixin (the "Magic" inside DeleteView), self.object is a specific "label" Django uses to store the database record the view is currently working on.

            # If you are deleting Article #5, self.object points to Article #5.

            # If you are deleting Article #9, self.object points to Article #9.


            # Below, not using self.object prevents confusion of the Django Convention, and also allows us to control the exact moment we fetch the object from the database, which is crucial for handling messages correctly.
            target = self.get_object()
            
            try:
                # 1. Perform the delete first
                target.delete()
                
                # 2. Add the message AFTER the successful DB operation
                messages.success(request, "Article Deleted Successfully!", extra_tags="destructive")
                
                # 3. Explicitly return a redirect
                return redirect(self.success_url)
                
            except ProtectedError:
                messages.error(request, "Cannot delete: This article is referenced in other places.")
            except ObjectDoesNotExist:
                messages.error(request, "Error: This article was already deleted by another user.")
            except (IntegrityError, DatabaseError):
                messages.error(request, "A system error occurred. Please try again later.")
            
            return redirect(self.success_url)


