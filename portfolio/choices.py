# PROFILE CHOICES
JOB_SPHERE_CHOICES = [
    ('cinema', 'Кино'),
    ('tv', 'Телевидение'),
    ('theatre', 'Театр'),
    ('videogames', 'Видеоигры'),
    ('corporate_video', 'Корпоративное видео'),
    ('advertising', 'Реклама'),
    ('education', 'Образование'),
]

EXPERIENCE_CHOICES = [
    ('over_6_years', 'Более 6 лет'),
    ('no_experience', 'Нет опыта'),
    ('3_to_6_years', 'От 3 до 6 лет'),
    ('1_to_3_years', 'От 1 года до 3 лет'),
]

SPECIALIZATION_CHOICES = [
    ('director_screenwriter', 'Режиссер, сценарист'),
    ('marketing_advertising_manager', 'Руководитель отдела маркетинга и рекламы'),
]

EMPLOYMENT_TYPE_CHOICES = [
    ('full_time', 'Полная занятость'),
    ('part_time', 'Частичная занятость'),
    ('project_work', 'Проектная работа'),
    ('internship', 'Стажировка'),
    ('volunteering', 'Волонтерство'),
]

WORK_SCHEDULE_CHOICES = [
    ('full_day', 'Полный день'),
    ('shift_schedule', 'Сменный график'),
    ('flexible_schedule', 'Гибкий график'),
    ('remote_work', 'Удаленная работа'),
    ('rotational_method', 'Вахтовый метод'),
]

SKILLS_CHOICES = [
    ('articulate_speech', 'Грамотная речь'),
    ('staff_management', 'Управление персоналом'),
    ('business_communication', 'Деловое общение'),
    ('project_management', 'Управление проектами'),
    ('information_processing', 'Работа с большим объемом информации'),
    ('creativity', 'Креативность'),
    ('staff_selection', 'Подбор персонала'),
    ('result_orientation', 'Ориентация на результат'),
    ('management_skills', 'Управленческие навыки'),
    ('staff_motivation', 'Мотивация персонала'),
    ('team_leadership', 'Руководство коллективом'),
]

# POST CHOICES
AGE_LIMITS = [
    ('0+', '0+'),
    ('6+', '6+'),
    ('12+', '12+'),
    ('16+', '16+'),
    ('18+', '18+'),
]

BUDGET = [
    ('', '-'),
    ('От 100 тыс до 1 млн', 'От 100 тыс до 1 млн'),
    ('От 1 млн до 10 млн', 'От 1 млн до 10 млн'),
    ('От 10 млн до 100 млн', 'От 10 млн до 100 млн'),
    ('Более 100 млн', 'Более 100 млн'),
]

PROJECT_TYPE_CHOICES = [
    ('interview', 'Интервью'),
    ('review', 'Рецензия'),
    ('shooting', 'Съемка'),
    ('trailers_and_announcements', 'Трейлеры и анонсы новых проектов'),
    ('awards_and_achievements', 'Информация о наградах и достижениях режиссера'),
    ('festivals_and_events', 'Фестивали и мероприятия'),
    ('educational_materials_and_lessons', 'Обучающие материалы и уроки'),
    ('personal_stories_and_interesting_facts', 'Личные истории и интересные факты из жизни'),
    ('scenario', 'Сценарий'),
    ('shooting_locations_and_schedules', 'Информация о местах съемок и графиках'),
    ('commercial', 'Рекламный ролик'),
    ('music_video', 'Музыкальный клип'),
    ('short_film', 'Короткометражный фильм'),
    ('feature_film', 'Полнометражный фильм'),
    ('tv_show', 'Телешоу'),
    ('web_series', 'Веб-сериал'),
]

PROJECT_GENRE_CHOICES = [
    ('family_drama', 'Семейная Драма'),
    ('historical_drama', 'Историческая Драма'),
    ('war_drama', 'Военная Драма'),
    ('criminal_drama', 'Криминальная Драма'),
    ('romantic_comedy', 'Романтическая Комедия'),
    ('black_comedy', 'Черная Комедия'),
    ('mystic', 'Мистика'),
    ('slasher', 'Слешер'),
    ('thriller', 'Триллер'),
    ('children', 'Детское'),
    ('educational', 'Образовательное'),
    ('entertainment', 'Развлекательное'),
    ('sci_fi', 'Научная Фантастика'),
    ('fantasy', 'Фентези'),
    ('biographical_documentary', 'Биографический Документальный Фильм'),
    ('nature_documentary', 'Природоведческий Документальный Фильм'),
    ('historical_documentary', 'Исторический Документальный Фильм'),
]

MUSIC_GENRE_CHOICES = [
    ('pop', 'Поп'),
    ('rock', 'Рок'),
    ('jazz', 'Джаз'),
    ('blues', 'Блюз'),
    ('classical', 'Классическая'),
    ('electronic', 'Электронная'),
    ('hip_hop', 'Хип-хоп'),
    ('rap', 'Рэп'),
    ('country', 'Кантри'),
    ('folk', 'Фолк'),
    ('r_and_b', 'R&B (Ритм-энд-блюз)'),
    ('reggae', 'Регги'),
    ('punk', 'Панк'),
    ('metal', 'Металл'),
    ('soul', 'Соул'),
    ('funk', 'Фонк'),
    ('disco', 'Диско'),
    ('techno', 'Техно'),
    ('dubstep', 'Дабстеп'),
    ('indie', 'Инди'),
    ('grunge', 'Гранж'),
    ('gospel', 'Госпел'),
    ('latin', 'Латиноамериканская музыка'),
    ('reggaeton', 'Реггетон'),
    ('k_pop', 'К-поп'),
]

RHYTHM_CHOICES = [
    ('fast_rhythm', 'Быстрый ритм'),
    ('slow_rhythm', 'Медленный ритм'),
    ('variable_rhythm', 'Переменный ритм'),
    ('rhythmic_editing', 'Ритмический монтаж'),
    ('parallel_editing', 'Параллельный монтаж'),
    ('insert_editing', 'Монтаж врезками'),
    ('leitmotif', 'Лейтмотив'),
]

STYLE_CHOICES = [
    ('documentary', 'Документальный'),
    ('pseudo_documentary', 'Псевдодокументальный'),
    ('author', 'Авторский'),
    ('experimental', 'Экспериментальный'),
    ('expressionism', 'Экспрессионизм'),
    ('surrealism', 'Сюрреализм'),
    ('noir', 'Нуар'),
    ('neorealism', 'Неореализм'),
    ('musical', 'Мюзикл'),
    ('realism', 'Реализм'),
    ('parody', 'Пародийный'),
    ('sarcastic', 'Саркастический'),
    ('tragic_melodramatic', 'Трагический Мелодраматический'),
]