from django.forms import ModelForm, widgets, CharField, IntegerField, Form
import logging
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Dataset, Metadata

from django.db import transaction

from leaflet.forms.widgets import LeafletWidget


class DatasetCreateForm(ModelForm):
    abstract = CharField(
        label="Description", widget=widgets.Textarea(attrs=dict(rows=2))
    )
    formation_period_start = IntegerField(label="Temporal start (year)")
    formation_period_end = IntegerField(label="Temporal end (year)")
    geographic_description = CharField(label="Geographic description")
    source = CharField(required=True, widget=widgets.Textarea(attrs=dict(rows=2)))

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit", css_class="mt-2"))

    def save(self, commit: bool = True):
        with transaction.atomic():
            instance = super().save(commit=False)
            instance.owner = self.user
            instance.public = False
            logging.warning(
                "This form will always commit, ensure you are using transaction.atomic to cancel this"
            )
            instance.save()

            instance.metadata.formation_period_start = date(
                self.cleaned_data["formation_period_start"], 1, 1
            )
            instance.metadata.formation_period_end = date(
                self.cleaned_data["formation_period_end"], 1, 1
            )
            instance.metadata.geographic_description = self.cleaned_data[
                "geographic_description"
            ]
            instance.metadata.abstract = self.cleaned_data["abstract"]
            instance.metadata.title = self.cleaned_data["name"]
            instance.metadata.save()

            return instance

    class Meta:
        model = Dataset
        fields = (
            "name",
            "source",
            "notes",
        )
        widgets = {
            "source": widgets.Textarea(
                {"rows": 2, "class": "textarea-bordered"},
            ),
            "notes": widgets.Textarea({"rows": 2, "class": "textarea-bordered"}),
        }


class DatasetFilterForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.add_input(Submit("submit", "Search", css_class="mt-2"))

    class Meta:
        widgets = {"my_datasets": widgets.CheckboxInput()}


class DatasetMetadataEditForm(ModelForm):
    source = CharField(required=False, widget=widgets.Textarea(attrs=dict(rows=2)))
    notes = CharField(required=False, widget=widgets.Textarea(attrs=dict(rows=2)))

    def __init__(self, *args, initial, instance, **kwargs):
        initial["source"] = instance.dataset.source
        initial["notes"] = instance.dataset.notes
        super().__init__(*args, initial=initial, instance=instance, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Submit", css_class="mt-2"))

    def save(self, commit: bool = True):
        with transaction.atomic():
            instance = super().save(commit=False)
            logging.warning(
                "This form will always commit, ensure you are using transaction.atomic to cancel this"
            )
            instance.save()
            instance.dataset.notes = self.cleaned_data["notes"]
            instance.dataset.source = self.cleaned_data["source"]
            instance.dataset.save(update_fields=["notes", "source"])
            return instance

    class Meta:
        model = Metadata
        fields = (
            "title",
            "abstract",
            "license",
            "language",
            "geographic_description",
            "formation_period_description",
            "formation_period_start",
            "formation_period_end",
            "date_publication",
            "maintenance_update_frequency",
            "maintenance_update_description",
            "bounding_box",
            "keywords",
            "taxonomies",
            "project_id",
            "project_title",
            "project_abstract",
            "project_study_area_description",
            "project_design_description",
        )
        widgets = {"bounding_box": LeafletWidget()}
