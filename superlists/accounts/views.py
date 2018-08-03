import sys
import uuid
from . import models
from superlists import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout


def send_login_email(request):
    email = request.POST.get('email', None)
    uid = str(uuid.uuid4())
    models.Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        settings.EMAIL_HOST_USER,
        [email]
    )
    return render(request, 'login_email_send.html')


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid', None)
    user = authenticate(uid=uid)

    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')