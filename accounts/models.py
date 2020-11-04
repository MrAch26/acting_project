from datetime import date, datetime

from django.contrib.auth import user_logged_in
from django.contrib.auth.models import AbstractUser, Permission, update_last_login
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_email_verification import sendConfirm
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


def no_future(value):
    today = date.today()
    if value > today:
        raise ValidationError('Date cannot be in the future.')

# def no_past(value):
#     today = date.today()
#     if value < today:
#         raise ValidationError('Date cannot be in the past.')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_actor = models.BooleanField(default=True)

    def profile(self):
        if self.is_actor:
            return self.actorprofile
        else:
            return self.agentprofile


class PhysicalInfo(models.Model):
    HAIR_CHOICES = [("black", "Black"), ("brown", "Brown"), ("blond", "Blond"), ("red", "Red")]
    EYES_CHOICES = [("blue", "Blue"), ("brown", "Brown"), ("green", "Green"), ("grey", "Grey")]
    TYPES_OF_HAIR = [("S", "Straight"), ("C", "Curly"), ("A", "Affro"), ("O", "Other")]
    SKIN_CHOICES = [("B", "Black"), ("W", "White"), ("DB", "Dark-Brown"), ("brown", "Brown"), ("LB", "Light-Brown")]

    hair_color = models.CharField(choices=HAIR_CHOICES, max_length=50, null=True)
    types_of_hair = models.CharField(choices=TYPES_OF_HAIR, max_length=50, null=True)
    eyes_color = models.CharField(choices=EYES_CHOICES, max_length=50, null=True)
    skin_color = models.CharField(choices=SKIN_CHOICES, max_length=50, null=True)
    height = models.IntegerField(null=True)
    actor_profile = models.OneToOneField('ActorProfile', on_delete=models.CASCADE)

class ActorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    agency = models.CharField(blank=True, max_length=100)
    birth_date = models.DateField(null=True, validators=[no_future])
    phone = PhoneNumberField(blank=True)
    is_from = models.ForeignKey('main.Location', models.CASCADE, null=True)
    education = models.TextField(null=True)
    picture = models.ImageField(upload_to='profile_pics/', default='static/images/profiledefault.jpeg')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def birthyear(self):
        return datetime.now().year - self.birth_date.year


class AgentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name_of_agent = models.CharField(max_length=100, blank=True)
    created_in = models.DateField(null=True, help_text="Enter the date of creation", validators=[no_future])
    website = models.URLField(blank=True)
    social_media = models.CharField(max_length=50, blank=True)
    is_from = models.ForeignKey('main.Location', models.CASCADE, null=True)
    picture = models.ImageField(upload_to='profile_pics_agent/', default='static/images/profiledefault.jpeg')


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    # def save(self, **kwargs):
    #     super().save()

class Project(models.Model):
    TYPE_PROJECT_CHOICES = [("movie", "Movie"), ("tv-show", "TV-Show"), ("play", "Theatrical Play"), ("other", "Other")]
    name = models.CharField(max_length=50)
    type_of_project = models.CharField(max_length=30, choices=TYPE_PROJECT_CHOICES, default='movie')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class WorkHistory(models.Model):
    ROLE_CHOICES = [("main", "Main"), ("sup", "Supporting"), ("extra", "Extra")]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role_type = models.CharField(default="extra", choices=ROLE_CHOICES, max_length=50)
    publish_date = models.DateField()
    actor_profile = models.ForeignKey(ActorProfile, on_delete=models.CASCADE)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, created, instance, **kwargs):
    if created:
        if instance.is_actor:
            ActorProfile.objects.create(user=instance)
        else:
            AgentProfile.objects.create(user=instance)
        sendConfirm(instance)

        permission = Permission.objects.get(name='Can add project')
        permission1 = Permission.objects.get(name='Can add location')
        instance.user_permissions.add(permission)
        instance.user_permissions.add(permission1)
