from dal import autocomplete
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.views.generic.base import View

from accounts.forms import UserSignupForm, EditActorProfile, EditAgentProfile, EditUser, WorkHistoryFormSet, \
    WorkHistoryForm
from accounts.models import ActorProfile, AgentProfile, Project


class UserSignUp(CreateView):
    template_name = "registration/signup.html"
    model = User
    form_class = UserSignupForm
    # success_url = reverse_lazy('home') redireect if actor or not
    failed_message = "The User couldn't be added"

    def get_success_url(self, **kwargs):
        if self.is_actor:
            return reverse_lazy('edit_profile')
        else:
            return reverse_lazy('edit_agent')

    # todo: redirect to update profile

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
            # messages.add_message(request, messages.INFO, 'You have created an Actor Account successfully')
            return redirect('home')

    form = WorkHistoryForm()
    context = {'user_form': user_edit_form, 'profile_form': profile_edit_form, 'formset': formset, 'form1': form}

    return render(request, 'accounts/edit_profile.html', context)


def agent_profile(request):
    user_edit_form = EditUser(request.POST or None, instance=request.user)
    agent_edit_form = EditAgentProfile(request.POST or None, instance=request.user.profile())

    if request.method == 'POST':
        if user_edit_form.is_valid() and agent_edit_form.is_valid():
            user = user_edit_form.save()
            profile_agent = agent_edit_form.save()
            # messages.add_message(request, messages.INFO, 'You have created an Actor Account successfully')
            return redirect('home')

    context = {'user_form': user_edit_form, 'agent_form': agent_edit_form}

    return render(request, 'accounts/edit_agent.html', context)

# def profile(request):


class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs



# todo: def request
# class ProfileView(DetailView):
#     model = AgentProfile, ActorProfile
#     template_name = 'registration/profile.html'

# class MyLoginView(LoginView):
