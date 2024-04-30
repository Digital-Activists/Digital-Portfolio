from django.contrib import messages
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import *
from .utils import PageTitleMixin, SOCIAL_NETWORKS


def index(request):
    return render(request, 'portfolio/plug-index.html', {'title': 'Home', 'social_networks': SOCIAL_NETWORKS})


class EditProfileView(LoginRequiredMixin, FormView):
    template_name = 'portfolio/settings-information.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_form = list(context['form'])
        context['form_photo_and_description'] = list_form[:2]
        context['form_contacts'] = list_form[2:5]
        context['form_scope_of_work'] = list_form[5:]
        context.update({'social_networks': SOCIAL_NETWORKS, 'form_add_social_network': AddSocialNetworkForm()})
        return context

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        kwargs.update({'instance': Profile.objects.get(user=self.request.user)})
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect('home')


class EditAccountInformationView(LoginRequiredMixin, FormView):
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


def change_user_email_and_password(request):
    if request.method == 'POST':
        email_form = ChangeEmailForm(request.POST, instance=request.user)
        password_form = CustomSetPasswordFormNoRequired(request.user, request.POST)
        if email_form.is_valid():
            email_form.save()
            messages.success(request, 'Ваша почта была обновлена')

        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Ваша пароль был обновлен')

    else:
        email_form = ChangeEmailForm(instance=request.user)
        password_form = CustomSetPasswordFormNoRequired(user=request.user)

    context = {
        'form_email': email_form,
        'form_password': password_form
    }

    return render(request, 'portfolio/settings-security.html', context)


class LoginUser(LoginView, PageTitleMixin):
    form_class = LoginUserForm
    template_name = 'portfolio/authorization.html'
    PageTitle = 'Страница регистрации и авторизации'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class EnterEmailToResetPassword(PasswordResetView, PageTitleMixin):
    form_class = EnterEmailToResetPasswordForm
    template_name = 'portfolio/reset-password.html'
    email_template_name = 'portfolio/email/password_reset_mail_v2.html'
    subject_template_name = 'portfolio/email/password_subject_reset_mail.txt'
    success_url = reverse_lazy('home')
    PageTitle = 'Страница запроса на сброс пароля'


class UserResetPasswordConfirm(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'portfolio/reset-password-confirm.html'
    success_url = reverse_lazy('login')
    PageTitle = 'Страница сброса пароля'


# TODO: подтверждение почты после регистрации
def register(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        profile_form = CreateProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['username']
            profile = Profile(user=user, **profile_form.cleaned_data)
            profile.social_links = {}
            profile.nickname = user_form.cleaned_data['username']
            user.save()
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = CreateUserForm()
        profile_form = CreateProfileForm()

    fields = list(user_form)[:3] + list(profile_form) + list(user_form)[3:]
    return render(request, 'portfolio/registration.html', {'form_fields': fields, 'title': 'Регистрация'})


@method_decorator(login_required, name='dispatch')
def submit_social_network(request):
    if request.method == 'POST':
        form = AddSocialNetworkForm(request.POST)
        if form.is_valid():
            social_network_name = form.cleaned_data['social_network']
            request.user.profile.social_links[social_network_name] = form.cleaned_data['link']
