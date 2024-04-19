from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

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


class EnterEmailToResetPassword(SuccessMessageMixin, PasswordResetView):
    form_class = EnterEmailToResetPasswordForm
    template_name = 'portfolio/Password-Recovery.html'
    success_url = reverse_lazy('home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'portfolio/email/password_subject_reset_mail.txt'
    email_template_name = 'portfolio/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Страница запроса на сброс пароля'})
        return context


class SetNewPassword(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = SetNewPasswordForm
    template_name = 'portfolio/Password-reset.html'
    success_url = reverse_lazy('login')
    success_message = "Пароль успешно сброшен"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Страница сброса пароля'})
        return context


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
