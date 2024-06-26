# Generated by Django 5.0.4 on 2024-06-17 09:58

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import portfolio.models
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
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('country', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['country', 'name'],
            },
        ),
        migrations.CreateModel(
            name='PostRhythm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Быстрый ритм', 'Быстрый ритм'), ('Медленный ритм', 'Медленный ритм'), ('Переменный ритм', 'Переменный ритм'), ('Ритмический монтаж', 'Ритмический монтаж'), ('Параллельный монтаж', 'Параллельный монтаж'), ('Монтаж врезками', 'Монтаж врезками'), ('Лейтмотив', 'Лейтмотив'), ('-', '-')], max_length=30, unique=True, verbose_name='Ритм')),
                ('description', models.CharField(max_length=100, verbose_name='Описание ритма')),
            ],
            bases=(portfolio.models.StrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProfileEmploymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Полная занятость', 'Полная занятость'), ('Частичная занятость', 'Частичная занятость'), ('Проектная работа', 'Проектная работа'), ('Стажировка', 'Стажировка'), ('Волонтерство', 'Волонтерство')], max_length=30, unique=True)),
            ],
            bases=(portfolio.models.StrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProfileSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Грамотная речь', 'Грамотная речь'), ('Управление персоналом', 'Управление персоналом'), ('Деловое общение', 'Деловое общение'), ('Управление проектами', 'Управление проектами'), ('Работа с большим объемом информации', 'Работа с большим объемом информации'), ('Креативность', 'Креативность'), ('Подбор персонала', 'Подбор персонала'), ('Ориентация на результат', 'Ориентация на результат'), ('Управленческие навыки', 'Управленческие навыки'), ('Мотивация персонала', 'Мотивация персонала'), ('Руководство коллективом', 'Руководство коллективом')], max_length=50, unique=True)),
            ],
            bases=(portfolio.models.StrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProfileWorkSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Полный день', 'Полный день'), ('Сменный график', 'Сменный график'), ('Гибкий график', 'Гибкий график'), ('Удаленная работа', 'Удаленная работа'), ('Вахтовый метод', 'Вахтовый метод')], max_length=30, unique=True)),
            ],
            bases=(portfolio.models.StrMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=120, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, max_length=700, verbose_name='Описание')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('budget', models.CharField(blank=True, choices=[('От 100 тыс до 1 млн', 'От 100 тыс до 1 млн'), ('От 1 млн до 10 млн', 'От 1 млн до 10 млн'), ('От 10 млн до 100 млн', 'От 10 млн до 100 млн'), ('Более 100 млн', 'Более 100 млн')], max_length=50, verbose_name='Бюджет в рублях')),
                ('post_type', models.CharField(blank=True, choices=[('Интервью', 'Интервью'), ('Рецензия', 'Рецензия'), ('Съемка', 'Съемка'), ('Трейлеры и анонсы новых проектов', 'Трейлеры и анонсы новых проектов'), ('Информация о наградах и достижениях режиссера', 'Информация о наградах и достижениях режиссера'), ('Фестивали и мероприятия', 'Фестивали и мероприятия'), ('Обучающие материалы и уроки', 'Обучающие материалы и уроки'), ('Личные истории и интересные факты из жизни', 'Личные истории и интересные факты из жизни'), ('Сценарий', 'Сценарий'), ('Информация о местах съемок и графиках', 'Информация о местах съемок и графиках'), ('Рекламный ролик', 'Рекламный ролик'), ('Музыкальный клип', 'Музыкальный клип'), ('Короткометражный фильм', 'Короткометражный фильм'), ('Полнометражный фильм', 'Полнометражный фильм'), ('Телешоу', 'Телешоу'), ('Веб-сериал', 'Веб-сериал')], max_length=50, verbose_name='Тип поста')),
                ('genre', models.CharField(blank=True, choices=[('Семейная Драма', 'Семейная Драма'), ('Историческая Драма', 'Историческая Драма'), ('Военная Драма', 'Военная Драма'), ('Криминальная Драма', 'Криминальная Драма'), ('Романтическая Комедия', 'Романтическая Комедия'), ('Черная Комедия', 'Черная Комедия'), ('Мистика', 'Мистика'), ('Слешер', 'Слешер'), ('Триллер', 'Триллер'), ('Детское', 'Детское'), ('Образовательное', 'Образовательное'), ('Развлекательное', 'Развлекательное'), ('Научная Фантастика', 'Научная Фантастика'), ('Фентези', 'Фентези'), ('Биографический Документальный Фильм', 'Биографический Документальный Фильм'), ('Природоведческий Документальный Фильм', 'Природоведческий Документальный Фильм'), ('Исторический Документальный Фильм', 'Исторический Документальный Фильм')], max_length=64, verbose_name='Жанр')),
                ('music_genre', models.CharField(blank=True, choices=[('Поп', 'Поп'), ('Рок', 'Рок'), ('Джаз', 'Джаз'), ('Блюз', 'Блюз'), ('Классическая', 'Классическая'), ('Электронная', 'Электронная'), ('Хип-хоп', 'Хип-хоп'), ('Рэп', 'Рэп'), ('Кантри', 'Кантри'), ('Фолк', 'Фолк'), ('R&B (Ритм-энд-блюз)', 'R&B (Ритм-энд-блюз)'), ('Регги', 'Регги'), ('Панк', 'Панк'), ('Металл', 'Металл'), ('Соул', 'Соул'), ('Фонк', 'Фонк'), ('Диско', 'Диско'), ('Техно', 'Техно'), ('Дабстеп', 'Дабстеп'), ('Инди', 'Инди'), ('Гранж', 'Гранж'), ('Госпел', 'Госпел'), ('Латиноамериканская музыка', 'Латиноамериканская музыка'), ('Реггетон', 'Реггетон'), ('К-поп', 'К-поп')], max_length=30, verbose_name='Жанр музыки')),
                ('style', models.CharField(blank=True, choices=[('Документальный', 'Документальный'), ('Псевдодокументальный', 'Псевдодокументальный'), ('Авторский', 'Авторский'), ('Экспериментальный', 'Экспериментальный'), ('Экспрессионизм', 'Экспрессионизм'), ('Сюрреализм', 'Сюрреализм'), ('Нуар', 'Нуар'), ('Неореализм', 'Неореализм'), ('Мюзикл', 'Мюзикл'), ('Реализм', 'Реализм'), ('Пародийный', 'Пародийный'), ('Саркастический', 'Саркастический'), ('Трагический Мелодраматический', 'Трагический Мелодраматический')], max_length=64, verbose_name='Стиль')),
                ('age_limit', models.CharField(blank=True, choices=[('0+', '0+'), ('6+', '6+'), ('12+', '12+'), ('16+', '16+'), ('18+', '18+')], max_length=3, verbose_name='Возрастное ограничение')),
                ('count_likes', models.IntegerField(default=0, verbose_name='Лайки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('liked_users', models.ManyToManyField(related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
                ('rhythm', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='portfolio.postrhythm', verbose_name='Ритм')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=portfolio.utils.get_path_to_post_files, validators=[django.core.validators.FileExtensionValidator(['pdf', 'ppt', 'pptx', 'doc', 'docx'])])),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='portfolio.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to=portfolio.utils.get_path_to_post_files)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='portfolio.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=portfolio.utils.get_path_to_post_files, validators=[django.core.validators.FileExtensionValidator(['mp4'])])),
                ('preview', models.ImageField(upload_to=portfolio.utils.get_path_to_post_files)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='portfolio.post')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileSocialNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Medium', 'Medium'), ('Tumblr', 'Tumblr'), ('ВКонтакте', 'ВКонтакте'), ('Мой Мир', 'Мой Мир'), ('GitHub', 'GitHub'), ('Boosty', 'Boosty'), ('Instagram', 'Instagram'), ('Одноклассники', 'Одноклассники'), ('Telegram', 'Telegram'), ('Facebook', 'Facebook'), ('Pinterest', 'Pinterest'), ('Twitch', 'Twitch'), ('YouTube', 'YouTube'), ('Reddit', 'Reddit'), ('Dribbble', 'Dribbble'), ('Linkedin', 'Linkedin'), ('Patreon', 'Patreon'), ('Discord', 'Discord'), ('Slack', 'Slack'), ('TikTok', 'TikTok'), ('Behance', 'Behance')], max_length=50)),
                ('link', models.URLField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_networks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patronymic', models.CharField(blank=True, max_length=50, verbose_name='Отчество')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('nickname', models.SlugField(unique=True, verbose_name='Никнейм')),
                ('text', models.TextField(blank=True, verbose_name='Описание профиля')),
                ('image', models.ImageField(null=True, upload_to='photos/avatars', verbose_name='Фото профиля')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='Номер телефона')),
                ('scope_of_work', models.CharField(blank=True, choices=[('Кино', 'Кино'), ('Телевидение', 'Телевидение'), ('Театр', 'Театр'), ('Видеоигры', 'Видеоигры'), ('Корпоративное видео', 'Корпоративное видео'), ('Реклама', 'Реклама'), ('Образование', 'Образование')], max_length=20, verbose_name='Сфера деятельности')),
                ('experience', models.CharField(blank=True, choices=[('Нет опыта', 'Нет опыта'), ('От 1 года до 3 лет', 'От 1 года до 3 лет'), ('От 3 до 6 лет', 'От 3 до 6 лет'), ('Более 6 лет', 'Более 6 лет')], max_length=20, verbose_name='Опыт работы')),
                ('specialization', models.CharField(blank=True, choices=[('Режиссер, сценарист', 'Режиссер, сценарист'), ('Руководитель отдела маркетинга и рекламы', 'Руководитель отдела маркетинга и рекламы')], max_length=40, verbose_name='Специализация')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='portfolio.city', verbose_name='Город')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('employment_type', models.ManyToManyField(to='portfolio.profileemploymenttype', verbose_name='Тип занятости')),
                ('skills', models.ManyToManyField(to='portfolio.profileskill', verbose_name='Ключевые навыки')),
                ('work_schedule', models.ManyToManyField(to='portfolio.profileworkschedule', verbose_name='График работы')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['user__last_name', 'user__first_name', 'patronymic'],
            },
        ),
    ]
