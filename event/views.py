from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import calendar
from datetime import datetime
from .models import Event
from .forms import EventCreationFormSingle

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/index.html")

def calendar_view(request, year = None, month = None):
    if year is None or month is None:
        day = datetime.today()
        year = day.year
        month = day.month

    year = int(year)
    month = int(month)

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    cal = calendar.Calendar(6)                          # 6, So sunday is the first. Maybe changed later.
    days_in_month = cal.monthdayscalendar(year, month)

    sorted_events = Event.objects.all().order_by("start_time")              # Sort event by time first
    all_events = sorted_events.filter(date__year=year, date__month=month, user=request.user)   
    # Get events connected to this year and month ||| AND ALSO user, added later after v0.2

    events_per_day = {}
    for event in all_events:
        day = event.date.day                    # get day of event date
        if day not in events_per_day:           # if this day isn't already in the list, 
            events_per_day[day] = []            # create list for that day
        events_per_day[day].append(event)       # add event into that day

    print(events_per_day)

    # Force Sunday to start first
    # Wouldn't have to do this if setfirstweek() actually work
    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    return render(request, 'event/calendar.html', {      
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'next_month': next_month,
        'prev_year': prev_year,
        'next_year': next_year,
        'month_name': calendar.month_name[month],
        'month_days': days_in_month,
        'day_names': day_names, 
        'events': events_per_day,
    })

def event_add(request):
    if request.method == "POST":
        form = EventCreationFormSingle(request.POST)
        if form.is_valid():
            Event.objects.create(date=request.POST["date"], 
                             start_time=request.POST["start_time"], 
                             end_time=request.POST["end_time"], 
                             text=request.POST["text"], 
                             user=request.user)
            return HttpResponseRedirect(reverse("event:calendar"))
    else:
        form = EventCreationFormSingle()

    return render(request, "event/eventadd.html", {
        "form": form,
    })
