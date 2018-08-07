from accounts import views
from django.urls import path
from django.contrib.auth.views import logout


urlpatterns = [
    path('send_login_email', views.send_login_email, name='send_login_email'),
    path('login', views.login, name='login'),
    path('logout', logout, {'next_page': '/'}, name='logout'),
]
