from django.db import models

from accounts.models import CustomUser, Project


class JobOpp(models.Model):
    ROLE_CHOICES = [("main", "Main"), ("sup", "Supporting"), ("extra", "Extra")]

    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type_of_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # age_wanted = models.    GIVE OPTION for 0-10/10-15/15-20/...
    date_of_job = models.DateTimeField()
    language = models.CharField(max_length=10)
    from_home = models.BooleanField()
    is_paid = models.BooleanField()

