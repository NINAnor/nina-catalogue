# Generated by Django 4.2.7 on 2023-12-08 10:55

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0089_log_entry_data_json_null_to_object"),
        ("wagtailimages", "0025_alter_image_file_alter_rendition_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="StandardPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("introduction", models.TextField(blank=True, help_text="Text to describe the page")),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "heading_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "heading_text",
                                            wagtail.blocks.CharBlock(form_classname="title", required=True),
                                        ),
                                        (
                                            "size",
                                            wagtail.blocks.ChoiceBlock(
                                                blank=True,
                                                choices=[
                                                    ("", "Select a header size"),
                                                    ("h2", "H2"),
                                                    ("h3", "H3"),
                                                    ("h4", "H4"),
                                                ],
                                                required=False,
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "paragraph_block",
                                wagtail.blocks.RichTextBlock(icon="pilcrow", template="blocks/paragraph_block.html"),
                            ),
                            (
                                "image_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("image", wagtail.images.blocks.ImageChooserBlock(required=True)),
                                        ("caption", wagtail.blocks.CharBlock(required=False)),
                                        ("attribution", wagtail.blocks.CharBlock(required=False)),
                                    ]
                                ),
                            ),
                            (
                                "block_quote",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("text", wagtail.blocks.TextBlock()),
                                        (
                                            "attribute_name",
                                            wagtail.blocks.CharBlock(
                                                blank=True, label="e.g. Mary Berry", required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "embed_block",
                                wagtail.embeds.blocks.EmbedBlock(
                                    help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
                                    icon="media",
                                    template="blocks/embed_block.html",
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                        verbose_name="Page body",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Landscape mode only; horizontal width between 1000px and 3000px.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("hero_text", models.CharField(help_text="Write an introduction for the bakery", max_length=255)),
                (
                    "hero_cta",
                    models.CharField(
                        help_text="Text to display on Call to Action", max_length=255, verbose_name="Hero CTA"
                    ),
                ),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            (
                                "heading_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "heading_text",
                                            wagtail.blocks.CharBlock(form_classname="title", required=True),
                                        ),
                                        (
                                            "size",
                                            wagtail.blocks.ChoiceBlock(
                                                blank=True,
                                                choices=[
                                                    ("", "Select a header size"),
                                                    ("h2", "H2"),
                                                    ("h3", "H3"),
                                                    ("h4", "H4"),
                                                ],
                                                required=False,
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "paragraph_block",
                                wagtail.blocks.RichTextBlock(icon="pilcrow", template="blocks/paragraph_block.html"),
                            ),
                            (
                                "image_block",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("image", wagtail.images.blocks.ImageChooserBlock(required=True)),
                                        ("caption", wagtail.blocks.CharBlock(required=False)),
                                        ("attribution", wagtail.blocks.CharBlock(required=False)),
                                    ]
                                ),
                            ),
                            (
                                "block_quote",
                                wagtail.blocks.StructBlock(
                                    [
                                        ("text", wagtail.blocks.TextBlock()),
                                        (
                                            "attribute_name",
                                            wagtail.blocks.CharBlock(
                                                blank=True, label="e.g. Mary Berry", required=False
                                            ),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "embed_block",
                                wagtail.embeds.blocks.EmbedBlock(
                                    help_text="Insert an embed URL e.g https://www.youtube.com/watch?v=SGJFWirQ3ks",
                                    icon="media",
                                    template="blocks/embed_block.html",
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                        verbose_name="Home content block",
                    ),
                ),
                (
                    "hero_cta_link",
                    models.ForeignKey(
                        blank=True,
                        help_text="Choose a page to link to for the Call to Action",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailcore.page",
                        verbose_name="Hero CTA link",
                    ),
                ),
                (
                    "image",
                    models.ForeignKey(
                        blank=True,
                        help_text="Homepage image",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="wagtailimages.image",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]