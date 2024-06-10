from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile, Category


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        default_categories = ['Entertainment', 'Food', 'Transportation', 'Health', 'Shopping', 'Savings']
        for new_category in default_categories:
            category_obj, created = Category.objects.get_or_create(name=new_category)
            profile.categories.add(category_obj)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
