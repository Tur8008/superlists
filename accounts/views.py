from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.urls import reverse


from accounts.models import Token

# Create your views here.


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + f'{token.uid}'
    )
    message_body = f'Use this link to login:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'no-reply@biz-intel.ru',
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to login."
    )
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    print('user is:', user, 'token is:', request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
