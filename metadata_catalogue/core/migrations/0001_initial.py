# Generated by Django 4.2.6 on 2023-10-25 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("django_q", "0014_schedule_cluster"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrmQExtension",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "orm_q",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="extension", to="django_q.ormq"
                    ),
                ),
            ],
        ),
    ]
