import datetime

from dal import autocomplete
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from accounts.forms import WorkHistoryFormSet, EditProject
from accounts.models import Project
from main.forms import JobOppForm
from main.models import JobOpp


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

            return redirect('home')

    return render(request, 'main/create_job_opp.html', {'form': create_job_form})


def details_job_opp(request, pk):
    # student = Student.objects.get(id=id)
    job_opp = get_object_or_404(JobOpp, id=pk)

    return render(request, 'main/job_opp_details.html', {"job": job_opp})


def update_job_opp(request, pk):
    if request.user.is_actor:
        return redirect('home')
    job_id = JobOpp.objects.get(id=pk)
    update_job_form = JobOppForm(request.POST or None, instance=request.user.profile())

    if request.method == 'POST':
        if update_job_form.is_valid():
            job_update = update_job_form.save()
            # messages.add_message(request, messages.INFO, 'You have created an Actor Account successfully')
            return redirect('home')
    else:
        return render(request, 'main/create_job_opp.html', {'form': update_job_form})


class JobOppList(ListView):
    model = JobOpp
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'job_opp'
        return context


class DeleteJobOpp(DeleteView):
    model = JobOpp
    success_url = reverse_lazy('job_opp')
    context_object_name = 'jobs'



