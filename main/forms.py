import datetime

from dal import autocomplete
from django import forms

from accounts.forms import DateInput
from .models import JobOpp, Participant


class JobOppForm(forms.ModelForm):
    class Meta:
        ordering = ['-id']
        model = JobOpp
        exclude = ['initiator']
        widgets = {
            'date_of_job': DateInput(),
            'project': autocomplete.ModelSelect2(url='project_autocomplete', attrs={'class': 'fix-height1'}),
            'location': autocomplete.ModelSelect2(url='location_autocomplete', attrs={'class': 'fix-height1'})
        }
        help_texts = {
            'project': 'Later on you will be able to update details of this project.',
        }
        labels = {
            'is_paid': 'Are you paying the actors ?',
            'from_home': 'Is the audition from home ?'
        }

class JobOppEditForm(forms.ModelForm):
    class Meta:
        model = JobOpp
        exclude = ['initiator']
        widgets = {
            'date_of_job': DateInput(),
            'project': autocomplete.ModelSelect2(url='project_autocomplete', attrs={'class': 'fix-height1'}),
            'location': autocomplete.ModelSelect2(url='location_autocomplete', attrs={'class': 'fix-height1'})
        }
        help_texts = {
            'project': "Click 'next' to update your Project.",
        }
        labels = {
            'is_paid': 'Are you paying the actors ?',
            'from_home': 'Is the audition from home ?'
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["applicant"]
