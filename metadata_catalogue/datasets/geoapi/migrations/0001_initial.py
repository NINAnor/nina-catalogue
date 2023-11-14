# Generated by Django 4.2.6 on 2023-11-13 12:28

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GeoAPIConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("max_records", models.IntegerField(default=10)),
                ("pretty_print", models.BooleanField(default=False)),
                ("map_url", models.URLField(default="https://tile.openstreetmap.org/{z}/{x}/{y}.png")),
                (
                    "map_attribution",
                    models.TextField(
                        default='&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
