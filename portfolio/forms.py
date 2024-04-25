from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

from .models import *


class CreateUserForm(UserCreationForm):
    username = forms.EmailField(label='Адрес электронной почты',
                                widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес электронной почты'}))
    last_name = forms.CharField(label='Фамилия', required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    first_name = forms.CharField(label='Имя', required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    password1 = forms.CharField(label='Пароль', required=True,  # help_text="Минимум 8 символов",
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


class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль', required=True,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}))
    new_password2 = forms.CharField(label='Подтверждение пароля', required=True,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['text', 'image', 'phone_number', 'email_public', 'city', 'scope_of_work']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.required = False
            if hasattr(self.instance.user, field_name):
                field.initial = getattr(self.instance.user, field_name)
            else:
                field.initial = getattr(self.instance.user.profile, field_name)


class EditAccountInformationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')

    class Meta:
        model = Profile
        fields = ['last_name', 'first_name', 'patronymic', 'date_of_birth', 'nickname']

    def __init__(self, *args, **kwargs):
        super(EditAccountInformationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.required = False
            if hasattr(self.instance.user, field_name):
                field.initial = getattr(self.instance.user, field_name)
            else:
                field.initial = getattr(self.instance.user.profile, field_name)

    def save(self, *args, **kwargs):
        instance = super(EditAccountInformationForm, self).save(*args, **kwargs)
        instance.user.first_name = self.cleaned_data['first_name']
        instance.user.last_name = self.cleaned_data['last_name']
        instance.user.save()
        return instance