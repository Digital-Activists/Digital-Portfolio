import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    date_of_birth = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return self.user.last_name + self.user.first_name + self.patronymic

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['user__last_name', 'user__first_name', 'patronymic']


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, **kwargs['request'].session)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    AGE_LIMITS = [('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')]

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    text = models.TextField(max_length=500, blank=True, verbose_name='Описание')
    date = models.DateField(default=now)
    budget = models.ForeignKey('PostBudget', null=True, on_delete=models.PROTECT)
    post_type = models.ForeignKey('PostType', null=True, on_delete=models.PROTECT)
    genre = models.ForeignKey('PostGenre', null=True, on_delete=models.PROTECT)
    style = models.ForeignKey('PostStyle', null=True, on_delete=models.PROTECT)
    age_limit = models.CharField(max_length=3, blank=True, choices=AGE_LIMITS, verbose_name='Возрастные ограничения')
    scope_of_work = models.ForeignKey('PostScopeOfWork', null=True, on_delete=models.PROTECT)


class PostBudget(models.Model):
    budget = models.CharField(max_length=50, verbose_name='Бюджет в рублях')


class PostType(models.Model):
    post_type = models.CharField(max_length=50, verbose_name='Тип проекта')


class PostGenre(models.Model):
    genre = models.CharField(max_length=50, verbose_name='Жанр проекта')


class PostStyle(models.Model):
    style = models.CharField(max_length=50, verbose_name='Стиль проекта')


class PostScopeOfWork(models.Model):
    scope_of_word = models.CharField(max_length=50, verbose_name='Сфера работы')
