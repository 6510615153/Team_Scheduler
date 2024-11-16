from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Event

@receiver(post_save, sender=Event)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Event.objects.create(date=instance.date, 
                             start_time=instance.start_time, 
                             endtime=instance.end_time, 
                             text=instance.text, 
                             user=instance)
