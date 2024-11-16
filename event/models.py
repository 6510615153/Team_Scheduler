from django.db import models
from django.core.exceptions import ValidationError
from users.models import Member
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    date = models.DateField("Day of Event")
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")
    text = models.TextField("Text", blank=True, null=True, max_length=20) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")        # Multiple Event, 1 user

    def __str__(self):
        return f"{self.start_time}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End Time can't be before Start Time.")
        