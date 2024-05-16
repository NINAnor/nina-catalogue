# Generated by Django 4.2.8 on 2024-05-15 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("maps", "0016_layer_metadata"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="rastersource",
            name="attribution",
        ),
        migrations.RemoveField(
            model_name="vectorsource",
            name="attribution",
        ),
        migrations.AddField(
            model_name="source",
            name="attribution",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]