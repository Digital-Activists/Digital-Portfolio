from django.db import migrations
from portfolio.choices import SKILLS_CHOICES, EMPLOYMENT_TYPE_CHOICES, WORK_SCHEDULE_CHOICES


def create_data(apps, schema_editor):
    ProfileSkill = apps.get_model('portfolio', 'ProfileSkill')
    ProfileEmploymentType = apps.get_model('portfolio', 'ProfileEmploymentType')
    ProfileWorkSchedule = apps.get_model('portfolio', 'ProfileWorkSchedule')

    for code, name in SKILLS_CHOICES:
        ProfileSkill.objects.create(name=name)

    for code, name in EMPLOYMENT_TYPE_CHOICES:
        ProfileEmploymentType.objects.create(name=name)

    for code, name in WORK_SCHEDULE_CHOICES:
        ProfileWorkSchedule.objects.create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
