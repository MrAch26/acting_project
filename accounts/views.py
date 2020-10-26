from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from accounts.forms import UserSignupForm


class UserSignUp(CreateView):
    template_name = "registration/signup.html"
    model = User
    form_class = UserSignupForm
    # success_url = reverse_lazy('home') redireect if actor or not
    failed_message = "The User couldn't be added"

    def form_valid(self, form):
        user_to_add = form.cleaned_data
        print("user_to_add", user_to_add)

        super(UserSignUp, self).form_valid(form)
        print("---------form valid")
        user = authenticate(self.request, username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
        if user.is_actor:


            return





# class ProfileView(UpdateView):
#     model = Profile
#     template_name = '../templates/profile.html'
#     form_class = ProfileViewForm
#     success_url = reverse_lazy('home')

# class MyLoginView(LoginView):
