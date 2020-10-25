from django import forms
from django.contrib.auth.forms import UserCreationForm  # form provided for registration

# SIGN UP
from accounts.models import Profile, CustomUser


class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class ProfileViewForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
