from django.urls import path
# from app.views import home
from app.views import ArticleCreateView, ArticleListView
from app.views import ArticleUpdateView, ArticleDeleteView


urlpatterns = [
    path("", ArticleListView.as_view(), name = 'home'),
    path("articles/create/", ArticleCreateView.as_view(), name="createArticle"),
    path("articles/<int:pk>/update/", ArticleUpdateView.as_view(), name="updateArticle"),
    path("articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="deleteArticle")
]
