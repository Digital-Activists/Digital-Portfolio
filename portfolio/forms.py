from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import *


class UserForm(UserCreationForm):
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


class ProfileForm(forms.ModelForm):
    patronymic = forms.CharField(label='Отчество',
                                 widget=forms.TextInput(attrs={'placeholder': 'Введите отчество, если есть'}))
    date_of_birth = forms.DateField(label='Дата рождения', required=True, input_formats=['%d.%m.%Y'],
                                    widget=forms.DateInput(attrs={'placeholder': 'дд.мм.гггг'}))

    class Meta:
        model = Profile
        fields = ['patronymic', 'date_of_birth']


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(label='Адрес электронной почты',
                                widget=forms.EmailInput(
                                    attrs={'placeholder': 'Введите адрес электронной почты', 'class': 'email-address'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'password'}))


class EmailRecoveryForm(forms.Form):
    email = forms.EmailField(label='Адрес электронной почты',
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(username=email).exists():
            raise ValidationError("Пользователь с таким email не зарегистрирован")


class ResetPasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='Новый пароль', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтверждение нового пароля', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
