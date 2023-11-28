# Generated by Django 4.2.7 on 2023-11-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0003_remove_person_unique_person"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="personrole",
            name="unique_role_per_person_in_metadata",
        ),
        migrations.AddConstraint(
            model_name="personrole",
            constraint=models.UniqueConstraint(
                models.F("person"), models.F("metadata"), models.F("role"), name="unique_role_per_person_in_metadata"
            ),
        ),
    ]