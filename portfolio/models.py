from django.contrib.auth.models import User
from django.db import models
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import now

from .utils import get_path_to_user_avatar


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    nickname = models.CharField(max_length=50, blank=True, unique=True, verbose_name='Никнейм')
    text = models.TextField(blank=True, verbose_name='Описание профиля')
    image = models.ImageField(upload_to=get_path_to_user_avatar, null=True, verbose_name='Фото профиля')
    phone_number = models.CharField(max_length=10, blank=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, blank=True, verbose_name='Город')
    scope_of_work = models.ForeignKey('ProfileScopeWork', null=True, on_delete=models.PROTECT,
                                      verbose_name='Сфера деятельности')
    social_links = models.JSONField(blank=True, verbose_name='Социальные сети')

    def __str__(self):
        return self.user.last_name + self.user.first_name + self.patronymic

    def get_absolute_url(self):
        if self.nickname != '':
            return reverse('portfolio:profile', kwargs={'nickname': self.nickname})
        return reverse('portfolio:profile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['user__last_name', 'user__first_name', 'patronymic']


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, **kwargs['request'].session)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Post(models.Model):
    AGE_LIMITS = [('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')]
    BUDGET = [('100тыс-1млн', 'От 100 тыс до 1 млн'), ('1млн-10млн', 'От 1 млн до 10 млн'),
              ('10млн-100млн', 'От 10 млн до 100 млн'), ('>100 млн', 'Более 100 млн')]

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    text = models.TextField(max_length=700, blank=True, verbose_name='Описание')
    date = models.DateField(default=now)
    budget = models.CharField(max_length=50, blank=True, choices=BUDGET, verbose_name='Бюджет в рублях')
    post_type = models.ForeignKey('PostType', null=True, on_delete=models.PROTECT)
    genre = models.ForeignKey('PostGenre', null=True, on_delete=models.PROTECT)
    style = models.ForeignKey('PostStyle', null=True, on_delete=models.PROTECT)
    age_limit = models.CharField(max_length=3, blank=True, choices=AGE_LIMITS, verbose_name='Возрастные ограничения')


class PostType(models.Model):
    post_type = models.CharField(max_length=50, verbose_name='Тип проекта')


class PostGenre(models.Model):
    genre = models.CharField(max_length=50, verbose_name='Жанр проекта')


class PostStyle(models.Model):
    style = models.CharField(max_length=50, verbose_name='Стиль проекта')


class ProfileScopeWork(models.Model):
    scope_of_word = models.CharField(max_length=50, verbose_name='Сфера работы')
