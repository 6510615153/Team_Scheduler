from event.models import Event
from datetime import datetime, timedelta
from django.utils import timezone
import django
import os
from time import sleep

from mailing import views

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schedule_project.settings')
django.setup()

def send_event_reminders():
        now = datetime.now()
        tomorrow = now + timedelta(hours=24)
        
        now = timezone.make_aware(now)
        tomorrow = timezone.make_aware(tomorrow)

        events = Event.objects.filter(date_time__range=(now, tomorrow), email_sent=False)

        for event in events:
            subject=f"Reminder for {event.text}"
            message=f"Your event '{event.text}' is happening soon!\n \
            Date: {event.date} \n \
            Start time: {event.start_time} | End time: {event.end_time}"
            to_email=[event.user.email]
        
            views.send(subject, message, to_email)

            event.email_sent = True
            event.save()
            print(f"Mail sent to {event.user}!")

while True:
    send_event_reminders()
    sleep(60*30)  # 60 = 1 minute 60*30 = 30 minutes