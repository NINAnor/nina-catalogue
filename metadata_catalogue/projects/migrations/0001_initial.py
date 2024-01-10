# Generated by Django 4.2.8 on 2024-01-09 15:11

import swapper
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        swapper.dependency('projects', 'Project'),
        swapper.dependency('projects', 'ProjectMembership'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "project",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=swapper.get_model_name('projects', 'Project')),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="projects_membership",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "swappable": swapper.swappable_setting('projects', 'ProjectMembership'),
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=250)),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=["name"]),
                ),
                (
                    "members",
                    models.ManyToManyField(blank=True, through=swapper.get_model_name('projects', 'ProjectMembership'), to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "swappable": swapper.swappable_setting('projects', 'Project'),
            },
        ),
        migrations.AddConstraint(
            model_name="projectmembership",
            constraint=models.UniqueConstraint(["project", "user"], name="unique user per project"),
        ),
    ]
