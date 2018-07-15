# from django.contrib import admin
from django.urls import path, include
from lists import urls as lists_urls
from lists import views as lists_views

urlpatterns = [
    path('', lists_views.home_page, name='home'),
    path('lists/', include(lists_urls))
]
