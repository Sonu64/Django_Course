from django.urls import path
from app.views import home, test


urlpatterns = [
    path("", home),
    # path("test", test),
    
]
