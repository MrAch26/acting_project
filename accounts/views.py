from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.views.generic.base import View

from accounts.forms import UserSignupForm, EditActorProfile, EditAgentProfile, EditUser, WorkHistoryFormSet, \
    WorkHistoryForm, EditProject, PhysicalInfoForm
from accounts.models import ActorProfile, AgentProfile, Project, CustomUser, WorkHistory, PhysicalInfo


class UserSignUp(SuccessMessageMixin, CreateView):
    template_name = "registration/signup.html"
    model = User
    form_class = UserSignupForm
    success_url = reverse_lazy('home')
    success_message = 'An email has been sent, please confirm your account and LOGIN'
    failed_message = "The User couldn't be added"

@login_required
def edit_agent_profile(request):
    if request.user.is_actor:
        return redirect('edit_actor')
    user_edit_form = EditUser(request.POST or None, instance=request.user)
    agent_edit_form = EditAgentProfile(request.POST or None, instance=request.user.profile())

    if request.method == 'POST':
        agent_edit_form = EditAgentProfile(request.POST, request.FILES, instance=request.user.profile())
        if user_edit_form.is_valid() and agent_edit_form.is_valid():
            user = user_edit_form.save()
            profile_agent = agent_edit_form.save()
            messages.add_message(request, messages.INFO, 'Successfully Updated !')
            return redirect(reverse_lazy('agent_profile', kwargs={'username': request.user.username}))

    context = {'user_form': user_edit_form, 'agent_form': agent_edit_form, 'nav': 'profile'}

    return render(request, 'accounts/edit_agent.html', context)

@login_required
def edit_actor_profile(request):
    if not request.user.is_actor:
        return redirect('edit_agent')
    user_edit_form = EditUser(request.POST or None, instance=request.user)
    profile_edit_form = EditActorProfile(instance=request.user.profile())
    physical_info, created = PhysicalInfo.objects.get_or_create(actor_profile=request.user.profile())
    physical_info_form = PhysicalInfoForm(request.POST or None, instance=physical_info)

    formset = WorkHistoryFormSet(request.POST or None)

    if request.method == 'POST':
        profile_edit_form = EditActorProfile(request.POST, request.FILES, instance=request.user.profile())
        if user_edit_form.is_valid() and profile_edit_form.is_valid() and physical_info_form.is_valid():
            user = user_edit_form.save()
            profile = profile_edit_form.save()
            physical_info = physical_info_form.save()
            messages.add_message(request, messages.INFO, 'You have updated success')
            return redirect(reverse_lazy('actor_profile', kwargs={'username': request.user.username}))

    work_history = request.user.profile()

    context = {
        'physical_form': physical_info_form,
        'user_form': user_edit_form,
        'profile_form': profile_edit_form,
        'formset': formset,
        'nav': 'profile',
        'work': work_history
    }

    return render(request, 'accounts/edit_actor.html', context)


class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

@login_required
def show_agent_profile(request, username):
    user = CustomUser.objects.get(username=username)
    profile = user.profile()

    if user.is_actor:
        return redirect('show_actor_profile', username)

    return render(request, 'accounts/agent_profile.html', {'info': profile})

@login_required
def show_actor_profile(request, username):
    user = CustomUser.objects.get(username=username)
    profile = user.profile()
    # physical_info_form = PhysicalInfoForm()

    if not user.is_actor:
        return redirect('show_agent_profile', username)

    formset = WorkHistoryFormSet(request.POST or None)

    if request.method == 'POST':
        if formset.is_valid() and request.user == user:
            for form in formset:
                workhistory = form.save(commit=False)
                workhistory.actor_profile = profile
                workhistory.project.description = form.cleaned_data['desc']
                workhistory.project.type_of_project = form.cleaned_data['type_of_project']
                workhistory.project.save()
                workhistory.save()

    return render(request, 'accounts/actor_profile.html', {'info': profile, 'formset': WorkHistoryFormSet()})


@method_decorator(login_required, name='dispatch')
class UpdateWorkHistory(UpdateView):
    model = WorkHistory
    form_class = WorkHistoryForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('profile', kwargs={'username': self.object.actor_profile.user.username})

    #
    # def get_context_data(self, **kwargs):
    #     context = super(UpdateWorkHistory, self).get_context_data(**kwargs)
    #     context['proj'] = EditProject
    #     return context


@method_decorator(login_required, name='dispatch')
class DeleteWorkHistory(DeleteView):
    model = WorkHistory
    fields = '__all__'

    def get_success_url(self, **kwargs):
        return reverse_lazy('actor_profile', kwargs={'username': self.object.actor_profile.user.username})



