from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import CustomUser, Project, AgentProfile, ActorProfile


def no_past(value):
    today = date.today()
    if value < today:
        raise ValidationError('Date cannot be in the past.')

class Location(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class JobOpp(models.Model):
    ROLE_CHOICES = [("main", "Main"), ("sup", "Supporting"), ("extra", "Extra")]
    LANGUAGE_CHOICES = [(word[0:3].lower(), word) for word in ['French', 'English', 'Hebrew', 'Arabic', 'Persian']]
    AGE_CHOICES = [(str(num), f"{num}-{num + 5}") for num in range(0, 121) if num % 5 == 0]
    GENDER_CHOICES = [('m', 'Male'), ('f', 'Female'), ('o', 'Other')]

    posted_at = models.DateField(auto_now_add=True)
    initiator = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type_of_role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    date_of_job = models.DateField(help_text='min. from Tomorrow', validators=[no_past])
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='m')
    age_wanted = models.CharField(choices=AGE_CHOICES, max_length=15, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, blank=True)
    from_home = models.BooleanField()
    is_paid = models.BooleanField()

    def __str__(self):
        return self.project.name

    def actors(self):
        return [participant.applicant for participant in self.participant_set.all()]

class Participant(models.Model):
    STATUS_CHOICES = [("Rel", "Relevant"), ("Not Rel", "Not Relevant"), ("W", "Waiting review")]

    job_opp = models.ForeignKey(JobOpp, on_delete=models.CASCADE)
    applicant = models.ForeignKey(ActorProfile, models.CASCADE)
    already_apply = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="W")

    def __str__(self):
        return self.applicant
