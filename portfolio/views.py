from django.contrib import messages
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from .forms import *
from .utils import SOCIAL_NETWORKS, ProfileSuccessUrlMixin, ContextUpdateMixin, GetProfileMixin


@login_required(login_url='login')
def index(request):
    return render(request, 'portfolio/plug-index.html',
                  context={'user_profile': Profile.objects.get(user=request.user)})


class CreatePostView(LoginRequiredMixin, CreateView, ContextUpdateMixin):
    PageTitle = 'Create Post'
    form_class = CreatePostForm
    template_name = 'portfolio/plug-form.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')
    raise_exception = True

    def form_valid(self, form):
        author = Profile.objects.get(user=self.request.user)
        new_post = form.save(commit=False)
        new_post.author = author
        new_post.save()

        for f in self.request.FILES.getlist('files'):
            PostPhoto.objects.create(file=f, post=new_post)

        return redirect(self.success_url)


class EditProfileView(GetProfileMixin, ProfileSuccessUrlMixin, UpdateView, LoginRequiredMixin):
    model = Profile
    template_name = 'portfolio/settings-information.html'
    form_class = EditProfileForm
    second_form_class = AddSocialNetworkForm
    custom_success_url = 'edit_settings_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        list_profile_form_fields = list(context['form'])

        context['form_photo_and_description'] = list_profile_form_fields[:2]
        context['form_contacts'] = list_profile_form_fields[2:5]
        context['form_scope_of_work'] = list_profile_form_fields[5:]
        context['social_networks'] = SOCIAL_NETWORKS

        if 'form_add_social_network' not in context:
            context['form_add_social_network'] = self.second_form_class(self.request.GET)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile_form = self.form_class(request.POST, instance=self.object)
        social_network_form = self.second_form_class(request.POST)

        if profile_form.is_valid() or social_network_form.is_valid():
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user.email = profile_form.cleaned_data['email']
                profile.user.save()
                profile.save()
                messages.success(self.request, 'Your profile has been updated.')
                # TODO: Если форма не прошла проверку, display: не none
            if social_network_form.is_valid():
                self.form_social_network_save(social_network_form)
                messages.success(self.request, 'Social network has been updated.')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=profile_form, form_add_social_network=social_network_form))

    def form_social_network_save(self, form):
        social_network_name = form.cleaned_data['social_network']
        profile = Profile.objects.get(user=self.request.user)
        profile.social_links[social_network_name] = form.cleaned_data['link']
        profile.save()

    def get_object(self, queryset=None):
        return self.request.user.profile


class EditAccountInformationView(GetProfileMixin, ProfileSuccessUrlMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditAccountInformationForm
    template_name = 'portfolio/settings-account.html'
    custom_success_url = 'edit_settings_account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.user.first_name = form.cleaned_data['first_name']
        form.instance.user.last_name = form.cleaned_data['last_name']
        form.instance.user.save()
        messages.success(self.request, 'Your account has been updated!')
        return response


class EditSecuritySettingsView(GetProfileMixin, ProfileSuccessUrlMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeEmailForm
    second_form_class = CustomSetPasswordFormNoRequired
    template_name = 'portfolio/settings-security.html'
    custom_success_url = 'edit_settings_security'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = Profile.objects.get(user=self.request.user)
        if 'form_email' not in context.keys():
            email_form = self.form_class(instance=self.request.user)
            context['form_email'] = email_form,
        if 'form_password' not in context.keys():
            password_form = self.second_form_class(user=self.request.user)
            context['form_password'] = password_form
        return context

    def get_object(self):
        nickname = self.kwargs.get('nickname')
        profile = get_object_or_404(Profile, nickname=nickname)
        return profile.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        email_form = self.form_class(request.POST, instance=self.object)
        password_form = self.second_form_class(self.object, self.request.POST)

        if email_form.is_valid() or password_form.is_valid():
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Ваша почта была обновлена')
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Ваша пароль был обновлен')
            update_session_auth_hash(request, password_form.user)
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form_email=email_form, form_password=password_form))


class LoginUser(LoginView, ContextUpdateMixin):
    form_class = LoginUserForm
    template_name = 'portfolio/authorization.html'
    PageTitle = 'Страница регистрации и авторизации'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class EnterEmailToResetPassword(PasswordResetView, ContextUpdateMixin):
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
            profile = Profile(user=user, **profile_form.cleaned_data)
            profile.social_links = {}
            user.save()
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        user_form = CreateUserForm()
        profile_form = CreateProfileForm()

    fields = list(user_form)[:3] + list(profile_form) + list(user_form)[3:]
    return render(request, 'portfolio/registration.html', {'form_fields': fields, 'title': 'Регистрация'})


class UserProfileView(GetProfileMixin, DetailView):
    model = Profile
    template_name = 'portfolio/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = Profile.objects.get(nickname=self.kwargs['nickname']).user
        context['user'] = user
        context['posts'] = Post.objects.filter(author=user)
        return context
