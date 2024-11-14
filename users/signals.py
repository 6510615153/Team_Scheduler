from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member, Group

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(member_user=instance, member_name=instance.username)
