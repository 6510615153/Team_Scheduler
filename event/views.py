from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import calendar
from datetime import datetime
from .models import Event

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
        prev_year = year - 1

    cal = calendar.Calendar(6)                          # 6, So sunday is the first. Maybe changed later.
    days_in_month = cal.monthdayscalendar(year, month)

    

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
    })