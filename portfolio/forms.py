import datetime
import os

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator

from .models import *
from .utils import check_social_link, check_social_lick_type


class ProfileAvatarImageWidget(forms.ClearableFileInput):
    template_name = 'portfolio/widgets/custom_image_widget.html'


class BaseFilledFieldsForm(forms.ModelForm):
    required_fields = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.required = self.required_fields
            if hasattr(self.instance, field_name):
                field.initial = getattr(self.instance, field_name)
            else:
                field.initial = getattr(self.instance.user, field_name)


def validate_file_extension(value, valid_extensions):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_files(value):
    valid_extensions = ['.ppt', '.docx', '.doc', '.pdf']
    validate_file_extension(value, valid_extensions)


def validate_image_and_video(value):
    valid_extensions = ['.', '.', '.', '.']
    validate_file_extension(value, valid_extensions)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreatePostForm(forms.ModelForm):
    images = MultipleFileField(widget=MultipleFileInput(attrs={}))
    files = MultipleFileField(validators=[FileExtensionValidator(['pdf', 'ppt', 'doc', 'docx'])],
                              widget=MultipleFileInput(attrs={}))
    videos = MultipleFileField(validators=[FileExtensionValidator(['mp4'])], widget=MultipleFileInput(attrs={}))
    tags = forms.ModelChoiceField(queryset=ProfileTag.objects.all())

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.required = False
        self.fields['title'].required = True

    class Meta:
        model = Post
        fields = ['title', 'text', 'date', 'budget', 'post_type', 'genre', 'style', 'age_limit', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': '', 'placeholder': ''}),
            'text': forms.Textarea(attrs={'class': '', 'placeholder': ''}),
            'date': forms.DateInput(attrs={'class': '', 'placeholder': ''}),
            'budget': forms.Select(attrs={'class': '', 'placeholder': ''}),
            'post_type': forms.Select(attrs={'class': '', 'placeholder': ''}),
            'genre': forms.Select(attrs={'class': '', 'placeholder': ''}),
            'style': forms.Select(attrs={'class': '', 'placeholder': ''}),
            'age_limit': forms.Select(attrs={'class': '', 'placeholder': ''}),
            'tags': forms.Select(attrs={'class': '', 'placeholder': ''}),
        }


class CreateUserForm(UserCreationForm):
    username = forms.EmailField(label='Адрес электронной почты',
                                widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес электронной почты'}))
    last_name = forms.CharField(label='Фамилия', required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    first_name = forms.CharField(label='Имя', required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    password1 = forms.CharField(label='Пароль', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'password1', 'password2']


class CreateProfileForm(forms.ModelForm):
    patronymic = forms.CharField(label='Отчество', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'Введите отчество, если есть'}))
    date_of_birth = forms.DateField(label='Дата рождения', required=True, input_formats=['%d.%m.%Y'],
                                    widget=forms.DateInput(attrs={'placeholder': 'дд.мм.гггг'}))

    def clean_date_of_birth(self):
        date = self.cleaned_data['date_of_birth']
        if date.year < datetime.datetime.now().year - 99:
            raise ValidationError('Некорректная дата рождения')
        return date

    class Meta:
        model = Profile
        fields = ['patronymic', 'date_of_birth']


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Адрес электронной почты',
                                widget=forms.EmailInput(
                                    attrs={'placeholder': 'Введите адрес электронной почты', 'class': 'email-Adress'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'password'}))


class EnterEmailToResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(username=email).exists():
            raise ValidationError("Пользователь с таким email не зарегистрирован")
        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль', required=True,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}))
    new_password2 = forms.CharField(label='Подтверждение пароля', required=True,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))


class EditProfileForm(BaseFilledFieldsForm, forms.ModelForm):
    required_fields = False
    text = forms.CharField(label='Описание профиля', widget=forms.TextInput(
        attrs={'placeholder': 'Добавьте описание к своему профилю...', 'class': 'profile-description'}))
    email = forms.EmailField(label='Публичная электронная почта', help_text='Будет отображаться в профиле',
                             widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес электронной почты'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17, label='Номер телефона',
                                   widget=forms.TextInput(
                                       attrs={'placeholder': '+70000000000', 'class': 'telephone'}))
    city = forms.CharField(max_length=30, label='Город', widget=forms.TextInput(
        attrs={'placeholder': 'Введите город', 'class': 'city'}))
    image = forms.ImageField(label='Фото профиля',
                             widget=ProfileAvatarImageWidget(
                                 attrs={'class': 'profile-image-input', 'placeholder': 'Загрузить'}))

    class Meta:
        model = Profile
        fields = ['image', 'text', 'phone_number', 'email', 'city', 'scope_of_work']


class EditAccountInformationForm(BaseFilledFieldsForm, forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Имя', widget=forms.TextInput(
        attrs={'placeholder': 'Введите имя', 'class': 'first-name'}))
    last_name = forms.CharField(max_length=30, label='Фамилия', widget=forms.TextInput(
        attrs={'placeholder': 'Введите фамилию', 'class': 'last-name'}))
    patronymic = forms.CharField(label='Отчество', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Введите отчество, если есть', 'class': 'middle-name'}))
    nickname = forms.SlugField(max_length=50, label='Никнейм', required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Введите свой никнейм', 'class': 'nickname'}))
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(attrs={'class': 'birth-date'},
                                                                                         years=range(
                                                                                             datetime.date.today().year - 99,
                                                                                             datetime.date.today().year)))

    class Meta:
        model = Profile
        fields = ['last_name', 'first_name', 'patronymic', 'date_of_birth', 'nickname']


class AddSocialNetworkForm(forms.ModelForm):
    type = forms.CharField(max_length=30, widget=forms.HiddenInput(attrs={'id': 'social-network-hidden-input'}))
    link = forms.URLField(label='Введите ссылку на вашу социальную сеть', required=False, widget=forms.URLInput(
        attrs={'class': 'social-network-link', 'id': 'social-network-input', 'placeholder': 'Вставьте ссылку...'}))

    class Meta:
        model = ProfileSocialNetwork
        fields = ['link', 'type']

    def clean(self):
        cleaned_data = super().clean()
        social_network_type = cleaned_data.get('type')
        link = cleaned_data.get('link')

        if not check_social_lick_type(social_network_type):
            raise ValidationError('Недопустимая соцсеть')

        if not check_social_link(social_network_type, link) and link != '':
            raise ValidationError('Ссылка не прошла проверку')

        return cleaned_data


class ChangeEmailForm(forms.ModelForm):
    username = forms.EmailField(label='Адрес электронной почты', required=False,
                                widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес электронной почты'}))

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Это поле обязательно для заполнения.')
        if username == self.instance.username:
            raise ValidationError('Почта не была изменена')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такая почта уже используется')
        return username


class CustomSetPasswordFormNoRequired(CustomSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if not password1 or not password2:
            raise ValidationError('Пароли не совпадают, либо пустые')
        return cleaned_data
