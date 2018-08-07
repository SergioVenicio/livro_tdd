from superlists import settings
from django.urls import reverse
from accounts.models import Token
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.shortcuts import render, redirect


def send_login_email(request):
    email = request.POST.get('email', None)
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in: \n\n{url}'

    send_mail(
        'Your login link for Superlists',
        message_body,
        settings.EMAIL_HOST_USER, [email]
    )

    messages.add_message(
        request, messages.SUCCESS,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token', None))
    if user is not None:
        auth.login(request, user)
    return redirect('/')