from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_email_verification import sendConfirm
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_actor = models.BooleanField(default=True)

    def profile(self):
        if hasattr(self, 'actor_profile'):
            return self.actor_profile
        else:
            return self.agent_profile


class HairColor(models.Model):
    HAIR_CHOICES = [("black", "Black"), ("brown", "Brown"), ("blond", "Blond"), ("red", "Red")]
    name = models.CharField(choices=HAIR_CHOICES, max_length=50)


class EyesColor(models.Model):
    EYES_CHOICES = [("blue", "Blue"), ("brown", "Brown"), ("green", "Green"), ("grey", "Grey")]
    name = models.CharField(choices=EYES_CHOICES, max_length=50)


class TypesOfHair(models.Model):
    TYPES_OF_HAIR = [("S", "Straight"), ("C", "Curly"), ("A", "Affro"), ("O", "Other")]
    name = models.CharField(choices=TYPES_OF_HAIR, max_length=50)


class SkinColor(models.Model):
    SKIN_CHOICES = [("B", "Black"), ("W", "White"), ("DB", "Dark-Brown"), ("brown", "Brown"), ("LB", "Light-Brown")]
    name = models.CharField(choices=SKIN_CHOICES, max_length=50)


class WorkHistory(models.Model):
    pass


class ActorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    agency = models.CharField(blank=True, max_length=100)
    birth_date = models.DateField()
    phone = PhoneNumberField(blank=True)
    education = models.TextField()
    height = models.IntegerField()
    hair_color = models.ForeignKey(HairColor)
    eyes_color = models.ForeignKey(EyesColor)
    types_of_hair = models.ForeignKey(TypesOfHair)
    skin_color = models.ForeignKey(SkinColor)
    picture = models.ImageField(required=False)
    work_history = models.OneToOneField(WorkHistory)


class AgentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name_of_agent = models.CharField(max_length=100)
    created_in = models.DateField()
    website = models.URLField(blank=True)
    social_medias = models.TextField(blank=True)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, created, instance, **kwargs):
    if created:
        if instance.is_actor:
            ActorProfile.objects.create(user=instance)
        else:
            AgentProfile.objects.create(user=instance)
        sendConfirm(instance)

