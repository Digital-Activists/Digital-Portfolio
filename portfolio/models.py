from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# TODO: Хеширование пароля
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


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
