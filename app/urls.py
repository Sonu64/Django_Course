from django.urls import path
from app.views import home
from app.views import createArticle


urlpatterns = [
    path("", home, name = 'home'),
    path("articles/create/", createArticle, name = "createArticle")
]
