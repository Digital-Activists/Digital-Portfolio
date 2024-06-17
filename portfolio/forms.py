import datetime
from dateutil.relativedelta import relativedelta

from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q
from django.forms import widgets

from .models import *
from .utils import check_social_link, check_social_lick_type
from .form_utils import (
    ProfileAvatarImageWidget,
    CustomFileInput,
    MultipleFileField,
    MultipleFileInput,
)


class RequiredFieldsFormMixin:
    required_fields = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.required = self.required_fields


class BaseFilledFieldsForm(RequiredFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if hasattr(self.instance, field_name):
                field.initial = getattr(self.instance, field_name)
            else:
                field.initial = getattr(self.instance.user, field_name)


class UserPostForm(forms.ModelForm):
    videos = MultipleFileField(
        label="Видео",
        validators=[FileExtensionValidator(PostVideo.formats)],
        widget=CustomFileInput(
            style_class="input-file",
            hint="Разрешены форматы: {0}".format(", ".join(PostVideo.formats)),
        ),
    )
    images = MultipleFileField(
        label="Фотографии",
        validators=[validators.validate_image_file_extension],
        widget=CustomFileInput(
            style_class="input-file", hint="Разрешены форматы png, jpeg, jpg"
        ),
    )
    files = MultipleFileField(
        label="Документы",
        validators=[FileExtensionValidator(PostFile.formats)],
        widget=CustomFileInput(
            style_class="input-doc",
            hint="Разрешены форматы: {0}".format(", ".join(PostFile.formats)),
        ),
    )
    date = forms.DateField(
        label="Дата",
        initial=date.today,
        widget=forms.SelectDateWidget(
            attrs={"class": "birth-date"},
            years=range(
                datetime.date.today().year - 99, datetime.date.today().year + 1
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super(UserPostForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.required = False
        self.fields["title"].required = True

    class Meta:
        model = Post
        fields = [
            "title",
            "text",
            "date",
            "images",
            "videos",
            "files",
            "budget",
            "post_type",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "post-title", "placeholder": "Введите заголовок поста"}
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "post-description",
                    "placeholder": "Добавьте описание к своему посту описание",
                }
            ),
            "budget": forms.Select(attrs={"class": "post-type", "placeholder": ""}),
            "post_type": forms.Select(attrs={"class": "post-type", "placeholder": ""}),
            "budget": forms.Select(
                attrs={"class": "post-type", "placeholder": "Выберите бюджет в рублях"}
            ),
            "post_type": forms.Select(
                attrs={"class": "post-type", "placeholder": "Выберите тип поста"}
            ),
            "genre": forms.Select(attrs={"class": "", "placeholder": ""}),
            "style": forms.Select(attrs={"class": "", "placeholder": ""}),
            "age_limit": forms.Select(attrs={"class": "", "placeholder": ""}),
        }


class PostTagsForm(RequiredFieldsFormMixin, forms.ModelForm):
    required_fields = False

    rhythm = forms.ModelChoiceField(
        label="Ритм",
        queryset=PostRhythm.objects.all(),
        empty_label="-",
        widget=forms.RadioSelect(attrs={"class": "rhythm"}),
    )

    class Meta:
        model = Post
        fields = ["rhythm", "music_genre", "genre", "style", "age_limit"]
        widgets = {
            "rhythm": forms.RadioSelect(attrs={"class": "rhythm"}),
            "genre": forms.Select(
                attrs={"class": "project", "placeholder": "Выберите жанр проекта"}
            ),
            "music_genre": forms.Select(
                attrs={"class": "music", "placeholder": "Выберите жанр музыки"}
            ),
            "style": forms.Select(
                attrs={"class": "style", "placeholder": "Выберите стиль"}
            ),
            "age_limit": forms.Select(
                attrs={
                    "class": "age_limits",
                    "placeholder": "Выберите возрастное ограничение",
                }
            ),
        }


class SearchPostForm(RequiredFieldsFormMixin, forms.Form):
    required_fields = False
    title = forms.CharField(label="Заголовок")
    budget = forms.MultipleChoiceField(
        label="Бюджет",
        choices=BUDGET,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "", "placeholder": ""}),
    )
    post_type = forms.MultipleChoiceField(
        label="Тип поста",
        choices=PROJECT_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "", "placeholder": ""}),
    )

    def get_results(self):
        query = Q()
        for field in self.cleaned_data:
            if self.cleaned_data.get(field):
                query &= Q(**{f"{field}__icontains": self.cleaned_data.get(field)})

        return Post.objects.filter(query)


class CreateUserForm(UserCreationForm):
    username = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(
            attrs={"placeholder": "Введите адрес электронной почты"}
        ),
    )
    last_name = forms.CharField(
        label="Фамилия",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Введите фамилию"}),
    )
    first_name = forms.CharField(
        label="Имя",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Введите имя"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"}),
    )

    class Meta:
        model = User
        fields = ["username", "last_name", "first_name", "password1", "password2"]


class CreateProfileForm(forms.ModelForm):
    patronymic = forms.CharField(
        label="Отчество",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Введите отчество, если есть"}),
    )
    date_of_birth = forms.DateField(
        label="Дата рождения",
        required=True,
        input_formats=["%d.%m.%Y"],
        widget=forms.DateInput(attrs={"placeholder": "дд.мм.гггг"}),
    )

    def clean_date_of_birth(self):
        date = self.cleaned_data["date_of_birth"]
        if date.year < datetime.datetime.now().year - 99:
            raise ValidationError("Некорректная дата рождения")
        return date

    class Meta:
        model = Profile
        fields = ["patronymic", "date_of_birth"]


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Введите адрес электронной почты",
                "class": "email-Adress",
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Введите пароль", "class": "password"}
        ),
    )


class EnterEmailToResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="Адрес электронной почты",
        widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(username=email).exists():
            raise ValidationError("Пользователь с таким email не зарегистрирован")
        return email


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Введите новый пароль"}),
    )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}),
    )


class EditProfileForm(BaseFilledFieldsForm, forms.ModelForm):
    required_fields = False
    text = forms.CharField(
        label="Описание профиля",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Добавьте описание к своему профилю...",
                "class": "profile-description",
            }
        ),
    )
    email = forms.EmailField(
        label="Публичная электронная почта",
        help_text="Будет отображаться в профиле",
        widget=forms.EmailInput(
            attrs={"placeholder": "Введите адрес электронной почты"}
        ),
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        label="Номер телефона",
        widget=forms.TextInput(
            attrs={"placeholder": "+70000000000", "class": "telephone"}
        ),
    )
    image = forms.ImageField(
        label="Фото профиля",
        widget=ProfileAvatarImageWidget(
            attrs={"class": "profile-image-input", "placeholder": "Загрузить"}
        ),
    )

    class Meta:
        model = Profile
        fields = ["image", "text", "phone_number", "email", "city", "scope_of_work"]
        widgets = {
            "city": forms.Select(
                attrs={"placeholder": "Введите город", "class": "city"}
            )
        }


class EditProfileTagsForm(RequiredFieldsFormMixin, forms.ModelForm):
    required_fields = False

    class Meta:
        model = Profile
        fields = [
            "skills",
            "experience",
            "specialization",
            "employment_type",
            "work_schedule",
        ]
        widgets = {
            "skills": forms.CheckboxSelectMultiple(),
            "experience": forms.Select(
                attrs={"class": "list", "placeholder": "Укажите свой опыт работы"}
            ),
            "specialization": forms.Select(
                attrs={"class": "list", "placeholder": "Выберите свою специализацию"}
            ),
            "employment_type": forms.CheckboxSelectMultiple(),
            "work_schedule": forms.CheckboxSelectMultiple(),
        }


class EditAccountInformationForm(BaseFilledFieldsForm, forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        label="Имя",
        widget=forms.TextInput(
            attrs={"placeholder": "Введите имя", "class": "first-name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Фамилия",
        widget=forms.TextInput(
            attrs={"placeholder": "Введите фамилию", "class": "last-name"}
        ),
    )
    patronymic = forms.CharField(
        label="Отчество",
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите отчество, если есть", "class": "middle-name"}
        ),
    )
    nickname = forms.SlugField(
        max_length=50,
        label="Никнейм",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите свой никнейм", "class": "nickname"}
        ),
    )
    date_of_birth = forms.DateField(
        label="Дата рождения",
        widget=forms.SelectDateWidget(
            attrs={"class": "birth-date"},
            years=range(datetime.date.today().year - 99, datetime.date.today().year),
        ),
    )

    class Meta:
        model = Profile
        fields = ["last_name", "first_name", "patronymic", "date_of_birth", "nickname"]


class AddSocialNetworkForm(forms.ModelForm):
    type = forms.CharField(
        max_length=30,
        widget=forms.HiddenInput(attrs={"id": "social-network-hidden-input"}),
    )
    link = forms.URLField(
        label="Введите ссылку на вашу социальную сеть",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "social-network-link",
                "id": "social-network-input",
                "placeholder": "Вставьте ссылку...",
            }
        ),
    )

    class Meta:
        model = ProfileSocialNetwork
        fields = ["link", "type"]

    def clean(self):
        cleaned_data = super().clean()
        social_network_type = cleaned_data.get("type")
        link = cleaned_data.get("link")

        if not check_social_lick_type(social_network_type):
            raise ValidationError("Недопустимая соцсеть")

        if not check_social_link(social_network_type, link) and link != "":
            raise ValidationError("Ссылка не прошла проверку")

        return cleaned_data


class SearchUserForm(RequiredFieldsFormMixin, forms.Form):
    required_fields = False
    name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "search", "placeholder": "Поиск"}),
    )
    city = forms.ModelMultipleChoiceField(
        label="Город",
        queryset=City.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkselect", "placeholder": "Выбор города"}
        ),
    )
    age_from = forms.IntegerField(
        label="Возраст от",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={"class": "for-age", "placeholder": "От"}),
    )
    age_to = forms.IntegerField(
        label="Возраст до",
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={"class": "for-age", "placeholder": "До"}),
    )
    experience = forms.MultipleChoiceField(
        label="Опыт работы",
        choices=EXPERIENCE_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkselect", "placeholder": "Выбор опыта"}
        ),
    )
    scope_of_work = forms.MultipleChoiceField(
        label="Сфера деятельности",
        choices=JOB_SPHERE_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "checkselect",
                "placeholder": "Выбор сферы деятельности",
            }
        ),
    )
    specialization = forms.MultipleChoiceField(
        label="Специализация",
        choices=SPECIALIZATION_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkselect", "placeholder": "Выбор специализации"}
        ),
    )
    employment_type = forms.ModelMultipleChoiceField(
        label="Тип занятости",
        queryset=ProfileEmploymentType.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkselect", "placeholder": "Выбор типа занятости"}
        ),
    )
    work_schedule = forms.ModelMultipleChoiceField(
        label="График работы",
        queryset=ProfileWorkSchedule.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkselect", "placeholder": "Выбор графика работы"}
        ),
    )
    skills = forms.ModelMultipleChoiceField(
        label="Ключевые навыки",
        queryset=ProfileSkill.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "checkselect", "placeholder": "Выбор навыков"}
        ),
    )

    def get_results(self):
        user_query_dict = {}
        user_query = Q()

        name = self.cleaned_data["name"]

        if name.startswith("@"):
            user_query &= Q(profile__nickname__icontains=name)
        else:
            name_list = name.split(" ")
            additional_user_query = Q()

            for name_part in name_list:
                additional_user_query |= Q(last_name__icontains=name_part)
                additional_user_query |= Q(first_name__icontains=name_part)
                additional_user_query |= Q(profile__patronymic__icontains=name_part)

            user_query &= additional_user_query

        age_from = self.cleaned_data["age_from"]
        age_to = self.cleaned_data["age_to"]
        today = datetime.datetime.today()

        if age_from:
            age_from = today - relativedelta(years=age_from)
            user_query &= Q(profile__date_of_birth__lte=age_from)

        if age_to:
            age_to = today - relativedelta(years=age_to)
            user_query &= Q(profile__date_of_birth__gte=age_to)

        for field_name in self.cleaned_data.keys():
            if field_name in ["name", "age_from", "age_to"]:
                continue
            field_values = self.cleaned_data[field_name]
            if field_values:
                user_query &= Q(**{f"profile__{field_name}__in": field_values})

        user_objects = User.objects.filter(user_query).distinct()

        return user_objects


class ChangeEmailForm(forms.ModelForm):
    username = forms.EmailField(
        label="Адрес электронной почты",
        required=False,
        widget=forms.EmailInput(
            attrs={"placeholder": "Введите адрес электронной почты"}
        ),
    )

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise ValidationError("Это поле обязательно для заполнения.")
        if username == self.instance.username:
            raise ValidationError("Почта не была изменена")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Такая почта уже используется")
        return username


class CustomSetPasswordFormNoRequired(CustomSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
        self.fields["new_password1"].required = False
        self.fields["new_password2"].required = False

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if not password1 or not password2:
            raise ValidationError("Пароли не совпадают, либо пустые")
        return cleaned_data
