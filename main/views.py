import datetime
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView

from accounts.forms import EditProject
from accounts.models import Project
from main.forms import JobOppForm, JobOppEditForm, ParticipantForm
from main.models import JobOpp, Location, Participant


def index(request):
    context = {
        'nav': 'index',
        'midday': datetime.time(12),
        'evening': datetime.time(18)
    }
    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html', {'nav': 'about'})


def create_job_opp(request):
    if request.user.is_actor:
        return redirect('home')

    create_job_form = JobOppForm(request.POST or None)
    # proj_form = EditProject(request.POST or None)

    if request.method == 'POST':
        if create_job_form.is_valid():
            job = create_job_form.save(commit=False)
            job.initiator = request.user.profile()
            job.save()
            # proj_form = EditProject(request.POST, instance=job.project)
            # if proj_form.is_valid():
            #     proj_form.save()

            return redirect(reverse_lazy('details_job_opp', kwargs={'pk': job.id}))

    return render(request, 'main/create_job_opp.html', {'form': create_job_form})


def details_job_opp(request, pk):
    # student = Student.objects.get(id=id)
    job_opp = get_object_or_404(JobOpp, id=pk)

    return render(request, 'main/job_opp_details.html', {"job": job_opp})


def update_job_opp(request, pk):
    if request.user.is_actor:
        return redirect('home')
    job = JobOpp.objects.get(id=pk)
    update_job_form = JobOppEditForm(request.POST or None, instance=job)
    update_proj_form = EditProject(request.POST or None, instance=job.project)

    if request.method == 'POST':
        if update_job_form.is_valid():
            job_update = update_job_form.save()
            proj_update = update_proj_form.save()
            # messages.add_message(request, messages.INFO, 'You have created an Actor Account successfully')
            return redirect(reverse_lazy('details_job_opp', kwargs={'pk': job.id}))

    return render(request, 'main/update_job_opp.html', {'form': update_job_form, 'proj_form': update_proj_form})


class JobOppList(ListView):
    model = JobOpp
    context_object_name = 'jobs'
    ordering = ['-posted_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'job_opp'
        return context


class DeleteJobOpp(DeleteView):
    model = JobOpp
    success_url = reverse_lazy('job_opp')
    context_object_name = 'jobs'

class ProjectDetails(DetailView):
    model = Project
    context_object_name = 'projects'

class ProjectUpdate(UpdateView):
    model = Project
    context_object_name = 'projects'

class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Location.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


def apply_for_job(request, jobopp_id):
    if not request.user.is_actor:
        messages.add_message(request, messages.INFO, 'You cannot apply as an agent...')
        return redirect('job_opp')
    job = JobOpp.objects.get(id=jobopp_id)
    participant, created = Participant.objects.get_or_create(applicant=request.user.profile(), job_opp=job)

    return redirect('details_job_opp', jobopp_id)
