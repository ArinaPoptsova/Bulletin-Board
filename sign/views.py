import random

from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from .forms import VerificationForm, CreateUserForm
from .models import User


def register(request):
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            request.session['username'] = form.cleaned_data['username']
            code = str(random.randint(100000, 999999))
            request.session['code'] = code
            msg = EmailMultiAlternatives(
                subject='Код активации',
                body=code,
                from_email='lolkovalolka@yandex.ru',
                to=[form.cleaned_data['email']]
            )
            msg.send()
            return redirect('/verification/')
    return render(request, 'sign/register.html', {'form': form})


def verification(request):
    if not request.session['code']:
        return redirect('/signup/')
    form = VerificationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['code'] and form.cleaned_data['code'] == request.session['code']:
                user = User.objects.get(username=request.session['username'])
                user.is_active = True
                user.save()
                request.session['code'] = None
                request.session['username'] = None
                return redirect('/bulletins/')
            elif form.cleaned_data['code']:
                messages.error(request, 'Неверный код')
    user = User.objects.get(username=request.session['username'])
    return render(request, 'sign/verification.html', {'form': form, 'user': user})
