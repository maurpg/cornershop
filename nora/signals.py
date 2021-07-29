from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from nora.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    function to create user profile automatically a user is created
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    function to save instance of profile
    """
    instance.profile.save()
