from django import forms
from django.contrib.auth.forms import UserCreationForm  # form provided for registration
from django.forms import formset_factory
from .models import CustomUser, ActorProfile, AgentProfile, WorkHistory, PhysicalInfo, Project
from dal import autocomplete


class DateInput(forms.DateInput):
    input_type = 'date'


class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "is_actor"]
        labels = {
            "is_actor": "Are you an actor ?"
        }


class EditUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]


class EditActorProfile(forms.ModelForm):
    class Meta:
        model = ActorProfile
        exclude = ['user', 'physical_infos']


class EditAgentProfile(forms.ModelForm):
    class Meta:
        model = AgentProfile
        exclude = ['user']
        labels = {
            'name_of_agent': 'Name of the agency'
        }
        widgets = {
            'name_of_agent': forms.TextInput(attrs={'placeholder': 'if same leave blank'}),
            'created_in': DateInput()
        }


class PhysicalInfoForm(forms.ModelForm):
    class Meta:
        model = PhysicalInfo
        exclude = ['actor_profile']
        labels = {
            'height': 'Height (in cm)'
        }


class WorkHistoryForm(forms.ModelForm):
    TYPE_PROJECT_CHOICES = [("movie", "Movie"), ("tv-show", "TV-Show"), ("play", "Theatrical Play"), ("other", "Other")]
    desc = forms.CharField()
    type_of_project = forms.ChoiceField(choices=TYPE_PROJECT_CHOICES)

    class Meta:
        model = WorkHistory
        exclude = ['actor_profile']
        widgets = {
            'project': autocomplete.ModelSelect2(url='project_autocomplete'),
            'publish_date': DateInput()
        }


WorkHistoryFormSet = formset_factory(WorkHistoryForm, extra=0)


class EditProject(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['name']
        widgets = {
            'description': forms.Textarea(
                attrs={'placeholder': 'We are looking for... Our Movie/film is about...'}),

        }
