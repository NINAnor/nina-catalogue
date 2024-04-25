# Generated by Django 4.2.8 on 2024-03-05 10:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("maps", "0009_layer_is_basemap_layer_legend"),
    ]

    operations = [
        migrations.AddField(
            model_name="map",
            name="legend_config",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="layer",
            name="legend",
            field=models.JSONField(blank=True, null=True),
        ),
    ]