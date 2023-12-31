# Generated by Django 4.2.8 on 2023-12-21 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import metadata_catalogue.maps.models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("maps", "0004_map_visibility"),
    ]

    operations = [
        migrations.CreateModel(
            name="Portal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("title", models.CharField(max_length=250)),
                (
                    "visibility",
                    models.CharField(
                        choices=[("public", "Public"), ("private", "Private")], default="private", max_length=10
                    ),
                ),
                ("extra", models.JSONField(blank=True, default=metadata_catalogue.maps.models.empty_json)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PortalMap",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.IntegerField(blank=True, default=0)),
                ("extra", models.JSONField(blank=True, default=metadata_catalogue.maps.models.empty_json)),
                (
                    "map",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="portals", to="maps.map"
                    ),
                ),
                (
                    "portal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="maps", to="maps.portal"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="portal",
            constraint=models.UniqueConstraint(models.F("uuid"), name="portal_unique_uuid"),
        ),
    ]
