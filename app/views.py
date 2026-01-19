# from django.shortcuts import render
from django.http import HttpResponse
from app.models import Article
from django.shortcuts import render
import random


# Create your views here.

def home(request):
    allArticles = Article.objects.all() # Using Django ORM for the 1st time ⏰
    return render(request, "app/home.html", {"articles":allArticles})


