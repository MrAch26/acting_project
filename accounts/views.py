from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from accounts.forms import UserSignupForm, EditActorProfile, EditAgentProfile, EditUser, WorkHistoryFormSet


class UserSignUp(CreateView):
    template_name = "registration/signup.html"
    model = User
    form_class = UserSignupForm
    # success_url = reverse_lazy('home') redireect if actor or not
    failed_message = "The User couldn't be added"

    # def form_valid(self, form):
    #     user_to_add = form.cleaned_data
    #     print("user_to_add", user_to_add)
    #
    #     super(UserSignUp, self).form_valid(form)
    #     print("---------form valid")
    #     user = authenticate(self.request, username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password1'])
    #     if user.is_actor:
    #
    #
    #         return

def actor_profile(request):
    user_edit_form = EditUser(request.POST or None, instance=request.user)
    profile_edit_form = EditActorProfile(request.POST or None, instance=request.user.profile())

    # initial_data = []
    #
    # for workhistory in request.user.profile().workhistory_set.all():
    #     initial_data.append({
    #         'role_type': workhistory.role_type,
    #         'publish_date': workhistory.publish_date,
    #     })

    formset = WorkHistoryFormSet(request.POST or None, initial=request.user.profile().workhistory_set.all().values())

    if request.method == 'POST':
        if user_edit_form.is_valid() and profile_edit_form.is_valid() and formset.is_valid():
            user = user_edit_form.save()
            profile = profile_edit_form.save()
            for form in formset:
                workhistory = form.save(commit=False)
                workhistory.actor_profile = profile
                workhistory.save()
            return redirect('home')

    context = {'user_form': user_edit_form, 'profile_form': profile_edit_form, 'formset': formset}

    return render(request, 'accounts/edit_profile.html', context)



# class ProfileView(UpdateView):
#     model = Profile
#     template_name = '../templates/profile.html'
#     form_class = ProfileViewForm
#     success_url = reverse_lazy('home')

# class MyLoginView(LoginView):
