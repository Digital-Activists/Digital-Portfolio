from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from PIL import Image

from .utils import SOCIAL_NETWORKS, get_path_to_post_files


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    nickname = models.SlugField(max_length=50, unique=True, verbose_name='Никнейм')
    text = models.TextField(blank=True, verbose_name='Описание профиля')
    image = models.ImageField(upload_to='photos/avatars', null=True, verbose_name='Фото профиля')
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    scope_of_work = models.ForeignKey('ProfileScopeWork', null=True, on_delete=models.PROTECT,
                                      verbose_name='Сфера деятельности')

    def get_user_age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def save(self, *args, **kwargs):
        if not self.nickname and self.user.username:
            self.nickname = slugify(self.user.username)
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return f'{self.user.last_name} {self.user.first_name} {self.patronymic}'

    def get_absolute_url(self):
        return reverse('view_user_profile', kwargs={'nickname': self.nickname})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['user__last_name', 'user__first_name', 'patronymic']


class ProfileSocialNetwork(models.Model):
    type = models.CharField(choices=[(sn, sn) for sn in SOCIAL_NETWORKS.keys()], max_length=50)
    link = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_networks')

    def get_image_url(self):
        if self.type in SOCIAL_NETWORKS.keys():
            path = SOCIAL_NETWORKS[self.type]
            return path
        return ''


class ProfileTag(models.Model):
    tag = models.CharField(max_length=50, verbose_name='Тэг профиля')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.tag


class ProfileScopeWork(models.Model):
    scope_of_work = models.CharField(max_length=50, verbose_name='Сфера работы')

    def __str__(self):
        return self.scope_of_work


class Post(models.Model):
    AGE_LIMITS = [('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')]
    BUDGET = [('', '-'), ('От 100 тыс до 1 млн', 'От 100 тыс до 1 млн'), ('От 1 млн до 10 млн', 'От 1 млн до 10 млн'),
              ('От 10 млн до 100 млн', 'От 10 млн до 100 млн'), ('Более 100 млн', 'Более 100 млн')]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    text = models.TextField(max_length=700, blank=True, verbose_name='Описание')
    date = models.DateField(default=now, verbose_name='Дата')
    created_at = models.DateTimeField(auto_now_add=True)
    budget = models.CharField(max_length=50, blank=True, choices=BUDGET, verbose_name='Бюджет в рублях')
    post_type = models.ForeignKey('PostType', null=True, on_delete=models.PROTECT, verbose_name='Тип поста')
    genre = models.ForeignKey('PostGenre', null=True, on_delete=models.PROTECT, verbose_name='Жанр')
    style = models.ForeignKey('PostStyle', null=True, on_delete=models.PROTECT, verbose_name='Стиль')
    age_limit = models.CharField(max_length=3, blank=True, choices=AGE_LIMITS, verbose_name='Возрастные ограничения')
    post_slug = models.SlugField()

    class Meta:
        ordering = ['-created_at']


class PostPhoto(models.Model):
    file = models.ImageField(upload_to=get_path_to_post_files)
    post = models.ForeignKey(Post, related_name='photos', on_delete=models.CASCADE)


class PostVideo(models.Model):
    file = models.FileField(upload_to=get_path_to_post_files)
    post = models.ForeignKey(Post, related_name='videos', on_delete=models.CASCADE)


class PostFile(models.Model):
    file = models.FileField(upload_to=get_path_to_post_files)
    post = models.ForeignKey(Post, related_name='files', on_delete=models.CASCADE)


class PostType(models.Model):
    post_type = models.CharField(max_length=50, verbose_name='Тип проекта')

    def __str__(self):
        return self.post_type


class PostGenre(models.Model):
    genre = models.CharField(max_length=50, verbose_name='Жанр проекта')

    def __str__(self):
        return self.genre


class PostStyle(models.Model):
    style = models.CharField(max_length=50, verbose_name='Стиль проекта')

    def __str__(self):
        return self.style


class PostTag(models.Model):
    tag = models.CharField(max_length=50, verbose_name='Тэг поста')
    post = models.ForeignKey(Post, related_name='tags', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag
