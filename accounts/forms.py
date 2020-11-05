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
        fields = ["is_actor", "username", "email", "password1", "password2"]
        labels = {
            "is_actor": "Which side are you ? 😈"
        }
        help_texts = {
            'email': '<ul><li>An email will be sent for confirmation</li> <li>Please type a right email !</li></ul>'
        }
        widgets = {
            'is_actor1': forms.RadioSelect()
        }


class EditUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]


class EditActorProfile(forms.ModelForm):
    class Meta:
        model = ActorProfile
        exclude = ['user', 'physical_infos']
        widgets = {
            'is_from': autocomplete.ModelSelect2(url='location_autocomplete', attrs={'class': 'fix-height1'}),
            'birth_date': DateInput()
        }
        labels = {
            'is_from': 'Where are you from ? '
        }


class EditAgentProfile(forms.ModelForm):
    class Meta:
        model = AgentProfile
        exclude = ['user']
        labels = {
            'name_of_agent': 'Name of the agency',
            'is_from': 'Where are you from ? '
        }
        widgets = {
            'name_of_agent': forms.TextInput(attrs={'placeholder': 'if same leave blank'}),
            'created_in': DateInput(),
            'is_from': autocomplete.ModelSelect2(url='location_autocomplete', attrs={'class': 'fix-height1'})
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
            'project': autocomplete.ModelSelect2(url='project_autocomplete', attrs={'class': 'fix-height1'}),
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
