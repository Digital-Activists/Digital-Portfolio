from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import *


def index(request):
    return render(request, 'portfolio/index.html', {'title': 'Home'})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'portfolio/Registration and login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Страница регистрации и авторизации', 'form_login': self.get_form_class()})
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    return render(request, 'portfolio/Registration and login.html', {'title': 'Страница регистрации и авторизации'})


def reset_password(request):
    return render(request, 'portfolio/Password-reset.html', {'title': 'Reset Password'})


class EmailRecovery(FormView):
    form_class = EmailRecoveryForm
    template_name = 'portfolio/Email-recovery.html'
    success_url = reverse_lazy('enter_code_from_email')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Страница подтверждения почты'})
        return context


def email_recovery(request):
    return render(request, 'portfolio/Email-Recovery.html', {'title': 'Email Confirmation'})


def enter_code_from_email(request):
    return render(request, 'portfolio/Code-for-email.html', {'title': 'enter code from email'})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['username']
            profile = Profile(user=user, **profile_form.cleaned_data)
            user.save()
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    fields = list(user_form)[:3] + list(profile_form) + list(user_form)[3:]
    return render(request, 'portfolio/Registration.html', {'form_fields': fields, 'title': 'Регистрация'})
