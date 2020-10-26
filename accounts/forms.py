from django import forms
from django.contrib.auth.forms import UserCreationForm  # form provided for registration

# SIGN UP
from accounts.models import CustomUser


class UserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2", "is_actor"]

