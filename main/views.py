from dal import autocomplete
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from accounts.forms import EditProject
from accounts.models import Project, ActorProfile
from main.filter import JobOppFilter
from main.forms import JobOppForm, JobOppEditForm
from main.models import JobOpp, Location, Participant
from django.core.paginator import Paginator


def index(request):
    if not request.user.is_authenticated:
        context = {
            'nav': 'index',
        }
        return render(request, 'main/index.html', context)

    if request.user.is_actor:

        jobs = JobOpp.objects.all().order_by('-id')[:3]
        participants = request.user.profile().participant_set.all()
        paginator = Paginator(participants, 10)  # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'jobs': jobs, 'page_obj': page_obj}
        return render(request, 'main/actor_dash.html', context)
    else:
        new_actors = ActorProfile.objects.all().order_by('-id')[:3]
        jobs = request.user.profile().jobopp_set.all()
        paginator = Paginator(jobs, 10)  # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'new_actors': new_actors, 'page_obj': page_obj}
        return render(request, 'main/agent_dash.html', context)

def is_relevant(request, participant_id, relevant):
    participant = Participant.objects.get(pk=participant_id)

    if request.user.profile() != participant.job_opp.initiator:
        # messages
        return redirect("job_opp")

    if relevant:
        participant.status = "Rel"
        messages.add_message(request, messages.INFO, 'An email was sent to the user Successfully!')
        text_message = f'{participant.job_opp.initiator}, marqued your application as Relevvant he will get in touch with you soon is the agent'
        message = render_to_string('email/relevant_body.html', {'participant': participant})
        send_mail(
            f'An Agent is interested in your profile - {participant.job_opp.initiator}',
            text_message,
            settings.EMAIL_HOST_USER,
            [participant.applicant.user.email],
            html_message=message,
            fail_silently=False,
        )

        # destination email recipient

    else:
        participant.status = "Not Rel"

    participant.save()
    return redirect('details_job_opp', participant.job_opp.id)

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
            messages.add_message(request, messages.INFO, 'A new Job Opportunity was created !')
            return redirect(reverse_lazy('details_job_opp', kwargs={'pk': job.id}))

    return render(request, 'main/create_job_opp.html', {'form': create_job_form})

@login_required
def details_job_opp(request, pk):
    job_opp = get_object_or_404(JobOpp, id=pk)

    participant = Participant.objects.filter(job_opp=job_opp).order_by('-id')
    paginator = Paginator(participant, 10)  # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {"job": job_opp, "page_obj": page_obj}

    return render(request, 'main/job_opp_details.html', context)

@login_required
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
            messages.add_message(request, messages.INFO, 'Successfully Updated !')
            return redirect(reverse_lazy('details_job_opp', kwargs={'pk': job.id}))

    return render(request, 'main/update_job_opp.html', {'form': update_job_form, 'proj_form': update_proj_form})


class JobOppList(ListView):
    model = JobOpp
    context_object_name = 'jobs'
    ordering = ['-posted_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav'] = 'job_opp'
        context['filter'] = JobOppFilter(self.request.GET, queryset=self.get_queryset())
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
    messages.add_message(request, messages.INFO, 'You Applied Successfully !')

    return redirect('details_job_opp', jobopp_id)

