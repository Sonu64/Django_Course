from django.urls import path
from app.views import home
from app.views import ArticleCreateView


urlpatterns = [
    path("", home, name = 'home'),
    path("articles/create/", ArticleCreateView.as_view(), name = "createArticle")
]
