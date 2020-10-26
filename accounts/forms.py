from django import forms
from django.contrib.auth.forms import UserCreationForm  # form provided for registration
from .models import CustomUser, ActorProfile, AgentProfile, WorkHistory, PhysicalInfo


class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "is_actor"]

class EditUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name"]

class CreateActorProfile(forms.ModelForm):
    class Meta:
        model = ActorProfile
        exclude = ['user', 'physical_infos']


class CreateAgentProfile(forms.ModelForm):
    class Meta:
        model = AgentProfile
        exclude = ['user']

class PhysicalInfoForm(forms.ModelForm):
    class Meta:
        model = PhysicalInfo
        fields = '__all__'

class WorkHistoryForm(forms.ModelForm):
    class Meta:
        model = WorkHistory
        exclude = ['actor_profile']


