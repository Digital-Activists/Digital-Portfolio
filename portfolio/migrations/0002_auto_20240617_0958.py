from django.db import migrations
from portfolio.choices import (
    SKILLS_CHOICES,
    EMPLOYMENT_TYPE_CHOICES,
    WORK_SCHEDULE_CHOICES,
    RHYTHMS,
)

import csv


def create_data(apps, schema_editor):
    ProfileSkill = apps.get_model("portfolio", "ProfileSkill")
    ProfileEmploymentType = apps.get_model("portfolio", "ProfileEmploymentType")
    ProfileWorkSchedule = apps.get_model("portfolio", "ProfileWorkSchedule")
    PostRhythm = apps.get_model("portfolio", "PostRhythm")
    City = apps.get_model("portfolio", "City")

    for code, name in SKILLS_CHOICES:
        ProfileSkill.objects.create(name=name)

    for code, name in EMPLOYMENT_TYPE_CHOICES:
        ProfileEmploymentType.objects.create(name=name)

    for code, name in WORK_SCHEDULE_CHOICES:
        ProfileWorkSchedule.objects.create(name=name)

    for name, description in RHYTHMS.items():
        PostRhythm.objects.create(name=name, description=description)

    with open("portfolio/data/city.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Пропустить заголовки
        for row in reader:
            country = row[2]
            city_name = row[9]
            if city_name:
                _, created = City.objects.get_or_create(
                    country=country,
                    name=city_name,
                )


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_data),
    ]
