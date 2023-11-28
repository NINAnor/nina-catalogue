# Generated by Django 4.2.7 on 2023-11-28 11:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("datasets", "0002_alter_person_options_alter_personrole_options"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="person",
            name="unique_person",
        ),
        migrations.RunSQL("""
            create unique index if not exists unique_person on datasets_person (
                "first_name", "last_name", "position", "country_id", "belongs_to_id",
                "phone", "delivery_point", "city", "postal_code", "email"
            ) NULLS NOT DISTINCT
        """, "drop index unique_person")
    ]