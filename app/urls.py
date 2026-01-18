from django.urls import path
from app.views import home, test


urlpatterns = [
    path("root", home),
    path("test", test),
]
