from django.db import models
from accounts.models import CustomUser, Project, AgentProfile


class JobOpp(models.Model):
    ROLE_CHOICES = [("main", "Main"), ("sup", "Supporting"), ("extra", "Extra")]
    LANGUAGE_CHOICES = [(word[0:3].lower(), word) for word in ['French', 'English', 'Hebrew', 'Arabic', 'Persian']]
    AGE_CHOICES = [(str(num), f"{num}-{num+5}") for num in range(0, 121) if num % 5 == 0]
    GENDER_CHOICES = [('m', 'Male'), ('f', 'Female'), ('o', 'Other')]

    posted_at = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type_of_role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    date_of_job = models.DateTimeField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='m')
    age_wanted = models.CharField(choices=AGE_CHOICES, max_length=15, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, blank=True)
    from_home = models.BooleanField()
    is_paid = models.BooleanField()

    def __str__(self):
        return self.project.name


