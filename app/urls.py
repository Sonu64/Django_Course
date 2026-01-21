from django.urls import path
from app.views import home
from app.views import ArticleCreateView, ArticleListView


urlpatterns = [
    path("", ArticleListView.as_view(), name = 'home'),
    path("articles/create/", ArticleCreateView.as_view(), name = "createArticle")
]
