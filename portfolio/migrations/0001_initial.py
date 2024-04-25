# Generated by Django 5.0.4 on 2024-04-23 17:09

import django.db.models.deletion
import django.utils.timezone
import portfolio.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.CharField(max_length=50, verbose_name='Бюджет в рублях')),
            ],
        ),
        migrations.CreateModel(
            name='PostGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=50, verbose_name='Жанр проекта')),
            ],
        ),
        migrations.CreateModel(
            name='PostStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=50, verbose_name='Стиль проекта')),
            ],
        ),
        migrations.CreateModel(
            name='PostType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(max_length=50, verbose_name='Тип проекта')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileScopeWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope_of_word', models.CharField(max_length=50, verbose_name='Сфера работы')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patronymic', models.CharField(blank=True, max_length=50, verbose_name='Отчество')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('nickname', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Никнейм')),
                ('text', models.TextField(blank=True, verbose_name='Описание профиля')),
                ('image', models.ImageField(null=True, upload_to=portfolio.utils.get_path_to_user_avatar)),
                ('phone_number', models.CharField(blank=True, max_length=10, verbose_name='Номер телефона')),
                ('email_public', models.EmailField(blank=True, max_length=254, verbose_name='Почта для связи')),
                ('city', models.CharField(blank=True, max_length=50, verbose_name='Город')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('scope_of_work', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='portfolio.profilescopework')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['user__last_name', 'user__first_name', 'patronymic'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, max_length=500, verbose_name='Описание')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('age_limit', models.CharField(blank=True, choices=[('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')], max_length=3, verbose_name='Возрастные ограничения')),
                ('budget', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='portfolio.postbudget')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='portfolio.postgenre')),
                ('style', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='portfolio.poststyle')),
                ('post_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='portfolio.posttype')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='portfolio.profile')),
            ],
        ),
    ]