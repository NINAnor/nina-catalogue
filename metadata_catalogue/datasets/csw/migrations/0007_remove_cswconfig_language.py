# Generated by Django 4.2.7 on 2023-11-15 13:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("csw", "0006_remove_cswconfig_contact_address_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cswconfig",
            name="language",
        ),
    ]