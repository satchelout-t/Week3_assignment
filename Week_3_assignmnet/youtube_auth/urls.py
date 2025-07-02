# DjangoProjects/youtube_auth/urls.py

from django.contrib import admin
from django.urls import path, include 
from django.views.generic.base import RedirectView 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('', RedirectView.as_view(url='accounts/login/', permanent=False)),

]