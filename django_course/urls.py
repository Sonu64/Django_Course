"""
URL configuration for django_course project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='home')),
    path('articles/', include("app.urls")),
    path('accounts/', include('allauth.urls')),  # django-allauth URLs, no need for manual setup like a registrations/login.html...etc. allauth provides those pages out of the box. In the other HTML templates, we just have to use url 'account_login' to point to login page. and url 'account_logout' to point to logout page. Intially we did url 'logout OR login' but that was custom, now we are using allauth's built in logout/login page. Similar changes need to be done in settings.py to configure allauth. ex:- In LOGOUT_REDIRECT_URL etc.
    path('__debug__/', include("debug_toolbar.urls")),
]
