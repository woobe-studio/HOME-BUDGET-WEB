from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a profile for the user when a new user is created.

    Args:
        sender: The sender of the signal.
        instance: The instance of the user being saved.
        created (bool): Indicates whether the user is newly created.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    if created:
        profile = Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal receiver function to save the profile when the user is saved.

    Args:
        sender: The sender of the signal.
        instance: The instance of the user being saved.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    instance.profile.save()
