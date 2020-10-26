from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.forms import UserSignupForm, ProfileViewForm
from accounts.models import Profile

class UserSignUp(CreateView):
    template_name = "registration/signup.html"
    model = User
    form_class = UserSignupForm
    success_url = reverse_lazy('home')
    failed_message = "The User couldn't be added"

    # def form_valid(self, form):
    #     user_to_add = form.cleaned_data
    #     print("user_to_add", user_to_add)
    #
    #     super(UserSignUp, self).form_valid(form)
    #     print("---------form valid")
    #     user = authenticate(self.request, username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    #     if user is None:
    #         print("---------user none")
    #         return self.render_to_response(
    #             self.get_context_data(form=form,
    #                                   failed_message=self.failed_message))
    #
    #     else:
    #         print("-----------user good")
    #         sendConfirm(user)
    #         login(self.request, user)
    #         return redirect(reverse(self.get_success_url()))


class ProfileView(UpdateView):
    model = Profile
    template_name = '../templates/profile.html'
    form_class = ProfileViewForm
    success_url = reverse_lazy('home')

# class MyLoginView(LoginView):
