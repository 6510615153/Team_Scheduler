from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # the schedule table of another person
    # REQUIRE schedule models

    # time_table = models.............
    # schedule = models...................

class Group(models.Model):
    members = models.ManyToManyField(Account, blank=True, related_name="groupings")

    def __str__(self):
        return f"{self.members}"