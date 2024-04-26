from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import *


def index(request):
    return render(request, 'portfolio/plug-index.html', {'title': 'Home'})


@method_decorator(login_required, name='dispatch')
class EditProfileInformationView(FormView):
    template_name = 'portfolio/plug-form.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(EditProfileInformationView, self).get_form_kwargs()
        kwargs.update({'instance': Profile.objects.get(user=self.request.user)})
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class EditAccountInformationView(FormView):
    form_class = EditAccountInformationForm
    template_name = 'portfolio/settings-account.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(EditAccountInformationView, self).get_form_kwargs()
        kwargs.update({'instance': Profile.objects.get(user=self.request.user)})
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('home')


# class EditSecurityInformationView(FormView):
#     form_class = EditSecurityInformationForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'portfolio/authorization.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Страница регистрации и авторизации', 'form_login': self.get_form_class()})
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class EnterEmailToResetPassword(PasswordResetView):
    form_class = EnterEmailToResetPasswordForm
    template_name = 'portfolio/reset-password.html'
    email_template_name = 'portfolio/email/password_reset_mail_v2.html'
    subject_template_name = 'portfolio/email/password_subject_reset_mail.txt'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Страница запроса на сброс пароля'})
        return context


class UserResetPasswordConfirm(PasswordResetConfirmView):
    form_class = SetNewPasswordForm
    template_name = 'portfolio/reset-password-confirm.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Страница сброса пароля'})
        return context


def register(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['username']
            profile = Profile(user=user, **profile_form.cleaned_data)
            user.save()
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = CreateUserForm()
        profile_form = CreateProfileForm()

    fields = list(user_form)[:3] + list(profile_form) + list(user_form)[3:]
    return render(request, 'portfolio/registration.html', {'form_fields': fields, 'title': 'Регистрация'})
