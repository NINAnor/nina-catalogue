# Generated by Django 4.2.7 on 2023-12-04 12:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0004_remove_personrole_unique_role_per_person_in_metadata_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="public",
            field=models.BooleanField(default=True),
        ),
    ]
