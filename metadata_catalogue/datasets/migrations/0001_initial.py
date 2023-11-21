# Generated by Django 4.2.7 on 2023-11-21 07:26

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.comparison
import metadata_catalogue.core.fields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("countries_plus", "0005_auto_20160224_1804"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("languages_plus", "0004_auto_20171214_0004"),
    ]

    operations = [
        migrations.CreateModel(
            name="Citation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("identifier", models.CharField(blank=True, max_length=500, null=True)),
                ("text", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Dataset",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=250, verbose_name="Internal name")),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                ("source", models.URLField(blank=True, null=True)),
                ("fetch_url", models.URLField(blank=True, null=True, verbose_name="URL of the resource to fetch")),
                ("fetch_type", models.IntegerField(blank=True, choices=[(1, "DarwinCore Archive")], null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                ("last_modified_at", models.DateTimeField(auto_now=True, verbose_name="Last modified at")),
                ("validated_at", models.DateTimeField(blank=True, null=True, verbose_name="Validated at")),
                ("fetch_success", models.BooleanField(default=False)),
                ("fetch_message", models.TextField(blank=True, null=True)),
                ("last_fetch_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Dataset",
            },
        ),
        migrations.CreateModel(
            name="Keyword",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("definition", models.URLField(blank=True, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="License",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("url", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Metadata",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=500, null=True)),
                ("date_created", models.DateTimeField(blank=True, null=True)),
                ("logo_url", models.URLField(blank=True, null=True)),
                ("date_publication", models.DateField(blank=True, null=True)),
                ("abstract", models.TextField(blank=True, null=True)),
                ("maintenance_update_frequency", models.TextField(blank=True, null=True)),
                ("maintenance_update_description", models.TextField(blank=True, null=True)),
                ("geographic_description", models.TextField(blank=True, null=True)),
                ("bounding_box", django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
                ("formation_period_start", models.DateField(blank=True, null=True)),
                ("formation_period_end", models.DateField(blank=True, null=True)),
                ("formation_period_description", models.TextField(blank=True, null=True)),
                ("project_id", models.CharField(blank=True, max_length=250, null=True)),
                ("project_title", models.CharField(blank=True, max_length=250, null=True)),
                ("project_abstract", models.TextField(blank=True, null=True)),
                ("project_study_area_description", models.TextField(blank=True, null=True)),
                ("project_design_description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="MetadataIdentifier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("identifier", models.CharField(max_length=500)),
                (
                    "source",
                    models.CharField(blank=True, choices=[("IPT", "IPT"), ("GBIF", "GBIF")], max_length=5, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MethodStep",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.IntegerField(default=0)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(blank=True, max_length=150, null=True)),
                ("last_name", models.CharField(blank=True, max_length=150, null=True)),
                ("position", models.CharField(blank=True, max_length=250, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("city", models.TextField(blank=True, null=True)),
                ("delivery_point", models.TextField(blank=True, null=True)),
                ("postal_code", models.IntegerField(blank=True, null=True)),
                (
                    "belongs_to",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="datasets.organization"
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="countries_plus.country"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaxonomyType",
            fields=[
                ("name", models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Taxonomy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=250)),
                ("common", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "type",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="datasets.taxonomytype"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PersonRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(max_length=10)),
                ("description", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "metadata",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="people", to="datasets.metadata"
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="roles", to="datasets.person"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PersonIdentifier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(max_length=150)),
                ("value", models.CharField(max_length=250)),
                ("person", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="datasets.person")),
            ],
        ),
        migrations.CreateModel(
            name="OrganizationRole",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(max_length=250)),
                (
                    "metadata",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organizations",
                        to="datasets.metadata",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="roles", to="datasets.organization"
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="organization",
            constraint=models.UniqueConstraint(fields=("name",), name="unique_org_name"),
        ),
        migrations.AddField(
            model_name="metadataidentifier",
            name="metadata",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="datasets.metadata"),
        ),
        migrations.AddField(
            model_name="metadata",
            name="bibliography",
            field=models.ManyToManyField(blank=True, related_name="in_dataset_bibliography", to="datasets.citation"),
        ),
        migrations.AddField(
            model_name="metadata",
            name="citation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="cited_by_dataset",
                to="datasets.citation",
            ),
        ),
        migrations.AddField(
            model_name="metadata",
            name="dataset",
            field=metadata_catalogue.core.fields.AutoOneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="metadata",
                to="datasets.dataset",
            ),
        ),
        migrations.AddField(
            model_name="metadata",
            name="keywords",
            field=models.ManyToManyField(blank=True, to="datasets.keyword"),
        ),
        migrations.AddField(
            model_name="metadata",
            name="language",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="languages_plus.language"
            ),
        ),
        migrations.AddField(
            model_name="metadata",
            name="license",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="datasets.license"
            ),
        ),
        migrations.AddField(
            model_name="metadata",
            name="taxonomies",
            field=models.ManyToManyField(blank=True, to="datasets.taxonomy"),
        ),
        migrations.AddConstraint(
            model_name="license",
            constraint=models.UniqueConstraint(fields=("name",), name="unique_license_name"),
        ),
        migrations.AddConstraint(
            model_name="license",
            constraint=models.UniqueConstraint(fields=("url",), name="unique_license_url"),
        ),
        migrations.AddConstraint(
            model_name="license",
            constraint=models.UniqueConstraint(
                django.db.models.functions.comparison.Coalesce("name", models.Value("")),
                django.db.models.functions.comparison.Coalesce("url", models.Value("")),
                name="unique_license_row",
            ),
        ),
        migrations.AddConstraint(
            model_name="keyword",
            constraint=models.UniqueConstraint(
                models.F("name"),
                django.db.models.functions.comparison.Coalesce("definition", models.Value("")),
                name="unique_kw_name_definition",
            ),
        ),
        migrations.AddField(
            model_name="dataset",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="owned_datasets",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Owner",
            ),
        ),
        migrations.AddField(
            model_name="dataset",
            name="validated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="validated_datasets",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Validator",
            ),
        ),
        migrations.AddConstraint(
            model_name="citation",
            constraint=models.UniqueConstraint(fields=("identifier", "text"), name="unique_citation"),
        ),
        migrations.AddConstraint(
            model_name="taxonomy",
            constraint=models.UniqueConstraint(fields=("name", "type"), name="unique_taxonomy_name_type"),
        ),
        migrations.AddConstraint(
            model_name="personidentifier",
            constraint=models.UniqueConstraint(fields=("person", "type", "value"), name="unique_pers_identifier"),
        ),
        migrations.AddConstraint(
            model_name="person",
            constraint=models.UniqueConstraint(
                django.db.models.functions.comparison.Coalesce("first_name", models.Value("")),
                django.db.models.functions.comparison.Coalesce("last_name", models.Value("")),
                django.db.models.functions.comparison.Coalesce("position", models.Value("")),
                django.db.models.functions.comparison.Coalesce("country", models.Value("")),
                django.db.models.functions.comparison.Coalesce("email", models.Value("")),
                django.db.models.functions.comparison.Coalesce("belongs_to", models.Value(-1)),
                django.db.models.functions.comparison.Coalesce("phone", models.Value("")),
                django.db.models.functions.comparison.Coalesce("city", models.Value("")),
                django.db.models.functions.comparison.Coalesce("delivery_point", models.Value("")),
                django.db.models.functions.comparison.Coalesce("postal_code", models.Value(-1)),
                name="unique_person",
            ),
        ),
        migrations.AddConstraint(
            model_name="metadataidentifier",
            constraint=models.UniqueConstraint(fields=("identifier", "source"), name="unique_metadata_identifier"),
        ),
        migrations.AddConstraint(
            model_name="dataset",
            constraint=models.UniqueConstraint(fields=("fetch_url",), name="unique_dataset_source"),
        ),
        migrations.AddConstraint(
            model_name="dataset",
            constraint=models.UniqueConstraint(fields=("uuid",), name="unique_dataset_uuid"),
        ),
        migrations.AlterField(
            model_name="metadata",
            name="keywords",
            field=models.ManyToManyField(blank=True, related_name="metadatas", to="datasets.keyword"),
        ),
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
        migrations.AddConstraint(
            model_name="organizationrole",
            constraint=models.UniqueConstraint(
                models.F("organization_id"),
                models.F("metadata_id"),
                models.F("role"),
                name="unique_role_per_org_in_metadata",
            ),
        ),
        migrations.AddField(
            model_name="metadata",
            name="fts",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="metadata",
            name="xml",
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name="ServiceInfo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("identification_title", models.TextField(blank=True, default="", null=True)),
                ("identification_abstract", models.TextField(blank=True, default="", null=True)),
                ("identification_keywords", models.TextField(blank=True, default="", null=True)),
                ("identification_keywords_type", models.TextField(blank=True, default="", null=True)),
                ("identification_fees", models.TextField(blank=True, default="", null=True)),
                ("identification_accessconstraints", models.TextField(blank=True, default="", null=True)),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="datasets.person"
                    ),
                ),
                (
                    "license",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="datasets.license"
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="datasets.organization"
                    ),
                ),
                ("contact_hours", models.TextField(blank=True, default="", null=True)),
                ("contact_instructions", models.TextField(blank=True, default="", null=True)),
                ("language", models.CharField(blank=True, max_length=7, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="dataset",
            name="fetch_url",
            field=models.TextField(blank=True, null=True, verbose_name="URL of the resource to fetch"),
        ),
        migrations.AlterField(
            model_name="dataset",
            name="source",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Content",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("gdal_vrt_definition", models.TextField(blank=True, null=True)),
                (
                    "dataset",
                    metadata_catalogue.core.fields.AutoOneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="content", to="datasets.dataset"
                    ),
                ),
            ],
        ),
    ]
