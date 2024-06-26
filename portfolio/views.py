from django.contrib import messages
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView, TemplateView

from .forms import *
from .services import get_video_preview, open_video
from .utils import SOCIAL_NETWORKS, ProfileSuccessUrlMixin, ContextUpdateMixin, GetProfileMixin, ProfileContextMixin


@login_required(login_url='login')
def index(request):
    return render(request, 'portfolio/plug/plug-index.html',
                  context={'user_profile': Profile.objects.get(user=request.user)})


class CreatePostView(GetProfileMixin, ProfileSuccessUrlMixin, LoginRequiredMixin, ContextUpdateMixin, CreateView):
    PageTitle = 'Create Post'
    form_class = UserPostForm
    template_name = 'portfolio/post-edit.html'
    custom_success_url = 'edit_post'
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.profile
        context['post_is_created'] = False
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        for image in self.request.FILES.getlist('images'):
            PostPhoto.objects.create(post=post, file=image)
        for video in self.request.FILES.getlist('videos'):
            PostVideo.objects.create(post=post, file=video, preview=get_video_preview(video))
        for file in self.request.FILES.getlist('files'):
            PostFile.objects.create(post=post, file=file)

        messages.success(self.request, 'Ваш пост создан и опубликован')
        return redirect('edit_post', post.post_slug)


class EditPostMixin(GetProfileMixin, ProfileSuccessUrlMixin, LoginRequiredMixin, UpdateView):
    raise_exception = True
    custom_success_url = 'view_user_profile'

    def get_object(self, queryset=None):
        post_slug = self.kwargs.get('post_slug')
        return get_object_or_404(Post, post_slug=post_slug, author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['post_is_created'] = True
        return context


class EditPostView(EditPostMixin):
    form_class = UserPostForm
    template_name = 'portfolio/post-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        form.fields['images'].initial = PostPhoto.objects.filter(post=self.object, post__author=self.request.user)
        context['videos'] = PostVideo.objects.filter(post=self.object, post__author=self.request.user)
        context['files'] = PostFile.objects.filter(post=self.object, post__author=self.request.user)
        return context

    def form_valid(self, form):
        post = self.object

        for image in form.cleaned_data['images']:
            print(image)

        for image in self.request.FILES.getlist('images'):
            print(image)
            # PostPhoto.objects.create(post=post, file=image)
        # for video in self.request.FILES.getlist('videos'):
        # PostVideo.objects.create(post=post, file=video, preview=get_video_preview(video))
        # for file in self.request.FILES.getlist('files'):
        # PostFile.objects.create(post=post, file=file)

        return redirect('edit_post', post.post_slug)


class EditPostTagsView(EditPostMixin):
    form_class = PostTagsForm
    template_name = 'portfolio/post-tags-edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rhythms'] = {rhythm.name: rhythm.description for rhythm in PostRhythm.objects.all()}
        return context


class EditProfileView(GetProfileMixin, ProfileContextMixin, ProfileSuccessUrlMixin, UpdateView, LoginRequiredMixin):
    model = Profile
    template_name = 'portfolio/settings/settings-information.html'
    form_class = EditProfileForm
    second_form_class = AddSocialNetworkForm
    custom_success_url = 'edit_settings_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        list_profile_form_fields = list(context['form'])

        context['form_photo'] = list_profile_form_fields[0]
        context['form_description'] = list_profile_form_fields[1]
        context['form_contacts'] = list_profile_form_fields[2:5]
        context['form_scope_of_work'] = list_profile_form_fields[5:]
        context['social_networks'] = SOCIAL_NETWORKS

        context['form_add_social_network'] = self.get_form(self.second_form_class)
        context['user_social_networks'] = ProfileSocialNetwork.objects.filter(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile_form = self.form_class(request.POST, request.FILES, instance=self.object)
        social_network_form = self.second_form_class(request.POST)

        # TODO: Если форма не прошла проверку, display: не none
        if social_network_form.is_valid():
            self.form_social_network_save(social_network_form)
            messages.success(self.request, f'Социальная сеть обновлена.')
            return HttpResponseRedirect(self.get_success_url())
        elif profile_form.is_valid():
            if 'image-clear' in request.POST:
                self.object.image.delete(save=False)
                self.object.image = None
                self.object.save()
            elif profile_form.has_changed():
                profile_form.save()
                self.object.user.email = profile_form.cleaned_data['email']
                self.object.user.save()
            messages.success(self.request, 'Ваш профиль был обновлен.')
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=profile_form))

    def form_social_network_save(self, form):
        if form.cleaned_data['link'] == '':
            social_network = ProfileSocialNetwork.objects.get(user=self.request.user, type=form.cleaned_data['type'])
            social_network.delete()
        else:
            social_network = form.save(commit=False)
            social_network.user = self.request.user
            social_network.save()

    def get_object(self, queryset=None):
        return self.request.user.profile


class EditAccountInformationView(GetProfileMixin, ProfileContextMixin, ProfileSuccessUrlMixin, LoginRequiredMixin,
                                 UpdateView):
    model = Profile
    form_class = EditAccountInformationForm
    template_name = 'portfolio/settings/settings-account.html'
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
        messages.success(self.request, 'Ваш аккаунт был обновлен!')
        return response


class EditSecuritySettingsView(GetProfileMixin, ProfileContextMixin, ProfileSuccessUrlMixin, LoginRequiredMixin,
                               UpdateView):
    model = User
    form_class = ChangeEmailForm
    second_form_class = CustomSetPasswordFormNoRequired
    template_name = 'portfolio/settings/settings-security.html'
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


class EditProfileTagsView(GetProfileMixin, ProfileContextMixin, ProfileSuccessUrlMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileTagsForm
    template_name = 'portfolio/settings/account-tags.html'
    custom_success_url = 'edit_settings_tags'

    def form_valid(self, form):
        messages.success(self.request, 'Ваш аккаунт был обновлен')
        return super().form_valid(form)


class LoginUser(LoginView, ContextUpdateMixin):
    form_class = LoginUserForm
    template_name = 'portfolio/authorization/authorization.html'
    PageTitle = 'Страница регистрации и авторизации'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class EnterEmailToResetPassword(PasswordResetView, ContextUpdateMixin):
    form_class = EnterEmailToResetPasswordForm
    template_name = 'portfolio/authorization/reset-password.html'
    email_template_name = 'portfolio/email/password_reset_mail_v2.html'
    subject_template_name = 'portfolio/email/password_subject_reset_mail.txt'
    success_url = reverse_lazy('home')
    PageTitle = 'Страница запроса на сброс пароля'


class UserResetPasswordConfirm(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'portfolio/authorization/reset-password-confirm.html'
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
            return redirect('view_user_profile', profile.nickname)
    else:
        user_form = CreateUserForm()
        profile_form = CreateProfileForm()

    fields = list(user_form)[:3] + list(profile_form) + list(user_form)[3:]
    return render(request, 'portfolio/authorization/registration.html', {'form_fields': fields, 'title': 'Регистрация'})


class UserProfileView(GetProfileMixin, ProfileContextMixin, DetailView):
    model = Profile
    template_name = 'portfolio/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object.user
        context['user'] = user
        context['posts'] = Post.objects.filter(author=user)
        return context

    def get_object(self):
        return Profile.objects.get(nickname=self.kwargs.get('nickname'))


@login_required(login_url='login')
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user != post.author:
        raise PermissionDenied
    post.delete()
    return redirect('view_user_profile', request.user.profile.nickname)


@login_required(login_url='login')
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author == request.user or post.liked_users.contains(request.user):
        raise PermissionDenied
    post.count_likes += 1
    post.liked_users.add(request.user)
    post.save()
    return redirect('view_user_profile', post.author.profile.nickname)


@login_required(login_url='login')
def dislike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author == request.user or not post.liked_users.contains(request.user):
        raise PermissionDenied
    post.count_likes -= 1
    post.liked_users.remove(request.user)
    post.save()
    return redirect('view_user_profile', post.author.profile.nickname)


class SearchMixin(ListView):
    form = None

    def get_queryset(self):
        self.form = self.form_class(self.request.GET or None)
        if self.form.is_valid():
            return self.form.get_results()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form or self.form_class()
        return context


class SearchPostView(SearchMixin):
    model = Post
    template_name = 'portfolio/search-post.html'
    form_class = SearchPostForm


class SearchUserView(SearchMixin):
    model = User
    template_name = 'portfolio/search-user.html'
    form_class = SearchUserForm


class GuidesView(TemplateView):
    template_name = 'portfolio/guides.html'


# TODO: ProfileFavouritePostsView, ProfileFavouriteUsersView
class ProfileFavouritePostsView(ListView, LoginRequiredMixin):
    model = Post
    template_name = 'portfolio/plug/plug-list.html'

    def get_queryset(self):
        return self.request.user.liked_posts.all()


class ProfileFavouriteUsersView(ListView, LoginRequiredMixin):
    model = User
    template_name = 'portfolio/plug/plug-list.html'

    # def get_queryset(self):
    #     return self.request.user.liked_users.all()


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_video(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
