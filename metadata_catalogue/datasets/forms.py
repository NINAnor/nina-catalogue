from django.forms import ModelForm, widgets, CharField, IntegerField, Form
import logging
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Dataset

from django.db import transaction


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
