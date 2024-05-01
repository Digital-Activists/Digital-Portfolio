import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

from .models import *


class BaseFilledFieldsForm(forms.ModelForm):
    required_fields = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.required = self.required_fields
            if hasattr(self.instance.user, field_name):
                field.initial = getattr(self.instance.user, field_name)
            else:
                field.initial = getattr(self.instance.user.profile, field_name)


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

    email = forms.EmailField(label='Адрес электронной почты, отображаемый в профиле',
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))

    class Meta:
        model = Profile
        fields = ['text', 'image', 'phone_number', 'email', 'city', 'scope_of_work']

    def save(self, *args, **kwargs):
        instance = super(EditProfileForm, self).save(*args, **kwargs)
        instance.user.email = self.cleaned_data['email']
        instance.user.save()
        return instance


class EditAccountInformationForm(BaseFilledFieldsForm, forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Имя', widget=forms.TextInput(
        attrs={'placeholder': 'Введите имя', 'class': 'first-name'}))
    last_name = forms.CharField(max_length=30, label='Фамилия', widget=forms.TextInput(
        attrs={'placeholder': 'Введите фамилию', 'class': 'last-name'}))
    patronymic = forms.CharField(label='Отчество', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Введите отчество, если есть', 'class': 'middle-name'}))
    nickname = forms.CharField(max_length=30, label='Никнейм', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Введите свой никнейм', 'class': 'nickname'}))
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(attrs={'class': 'birth-date'},
                                                                                         years=range(
                                                                                             datetime.date.today().year - 99,
                                                                                             datetime.date.today().year)))

    class Meta:
        model = Profile
        fields = ['last_name', 'first_name', 'patronymic', 'date_of_birth', 'nickname']

    def save(self, *args, **kwargs):
        instance = super(EditAccountInformationForm, self).save(*args, **kwargs)
        instance.user.first_name = self.cleaned_data['first_name']
        instance.user.last_name = self.cleaned_data['last_name']
        instance.user.save()
        return instance


class AddSocialNetworkForm(forms.Form):
    social_network = forms.CharField(max_length=30, widget=forms.HiddenInput(attrs={'id': 'social-network'}))
    link = forms.URLField(label='Лэйбл', widget=forms.URLInput(attrs={'class': 'social-network-link'}))


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
