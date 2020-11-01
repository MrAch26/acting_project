from dal import autocomplete
from django import forms

from accounts.forms import DateInput
from .models import JobOpp


class JobOppForm(forms.ModelForm):
    class Meta:
        ordering = ['-id']
        model = JobOpp
        exclude = ['initiator']
        widgets = {
            'date_of_job': DateInput(),
            'project': autocomplete.ModelSelect2(url='project_autocomplete'),
        }

