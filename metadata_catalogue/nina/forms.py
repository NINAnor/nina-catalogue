from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Project


class ProjectSearchForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["status", "topics", "category", "departments", "customer"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"

        self.helper.add_input(Submit("submit", "Search"))
