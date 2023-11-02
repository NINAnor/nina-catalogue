# Generated by Django 4.2.6 on 2023-11-02 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0002_alter_metadata_keywords"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personrole",
            name="role",
            field=models.CharField(
                choices=[
                    ("PROJ_PERS", "Project personnel"),
                    ("CONTACT", "Contact person"),
                    ("CREATOR", "Creator"),
                    ("PROVIDER", "Provider"),
                    ("ASSOCIATED", "Associated party"),
                ],
                max_length=10,
            ),
        ),
        migrations.AddConstraint(
            model_name="personrole",
            constraint=models.UniqueConstraint(
                models.F("person_id"),
                models.F("metadata_id"),
                models.F("role"),
                name="unique_role_per_person_in_metadata",
            ),
        ),
    ]
