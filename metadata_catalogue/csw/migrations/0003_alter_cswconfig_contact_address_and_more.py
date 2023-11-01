# Generated by Django 4.2.6 on 2023-10-31 12:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("csw", "0002_cswconfig_pretty_print"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_address",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_city",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_email",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_fax",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_hours",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_instructions",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_name",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_phone",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_position",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_postalcode",
            field=models.IntegerField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_role",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_stateorprovince",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="contact_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="identification_abstract",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="identification_accessconstraints",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="identification_fees",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="identification_keywords",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="identification_keywords_type",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="identification_title",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="profiles",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="provider_name",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="cswconfig",
            name="provider_url",
            field=models.URLField(blank=True, default="", null=True),
        ),
    ]
