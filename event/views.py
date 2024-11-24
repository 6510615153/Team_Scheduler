from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
import calendar
from datetime import datetime
from .models import Event
from .forms import EventCreationFormSingle
from users.models import Member, Joining, Group
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


# Create your views here.

@login_required
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

    # Force Sunday to start first
    # Wouldn't have to do this if setfirstweek() actually work
    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # packed_context = {      
    #     'year': year,
    #     'month': month,
    #     'prev_month': prev_month,
    #     'next_month': next_month,
    #     'prev_year': prev_year,
    #     'next_year': next_year,
    #     'month_name': calendar.month_name[month],
    #     'month_days': days_in_month,
    #     'day_names': day_names, 
    #     'events': events_per_day,
    # }

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
        # 'packed_context': packed_context
    })

@login_required
def event_add(request):
    if request.method == "POST":
        form = EventCreationFormSingle(request.POST)
        if form.is_valid():
            Event.objects.create(date=request.POST["date"], 
                             start_time=request.POST["start_time"], 
                             end_time=request.POST["end_time"], 
                             text=request.POST["text"], 
                             user=request.user,
                             member=Member.objects.get(member_user=request.user),
                             importance=request.POST["importance"],)
            return HttpResponseRedirect(reverse("event:calendar"))
    else:
        form = EventCreationFormSingle()

    return render(request, "event/eventadd.html", {
        "form": form,
    })

@login_required
def calendar_view_group(request, code, year = None, month = None):
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

    # Get current group that event is in

    current_group = Group.objects.get(group_code=code)

    current_join = Joining.objects.filter(joined_group = current_group).first().get_code()
    sorted_events = Event.objects.all().order_by("start_time")              # Sort event by time first
    all_events = sorted_events.filter(date__year=year, 
                                      date__month=month,)
    
    events_per_day = {}
    for event in all_events:
        day = event.date.day                    # get day of event date
        if day not in events_per_day:           # if this day isn't already in the list, 
            events_per_day[day] = []            # create list for that day

        current_event = event.member.joined_group.all()
        # print(event.member)
        # print(current_join)
        for item in current_event:
            #print(item.get_code())
            if item.get_code() == current_join:
                events_per_day[day].append(event) 


    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    return render(request, 'event/calendar_group.html', {      
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
        'group_code': code
    })

@login_required
def see_event_detail(request, event_id):
    current_event = Event.objects.get(pk=event_id)

    previous_url = request.META.get('HTTP_REFERER', '/calendar/')

    return render(request, 'event/event_page.html', {     
        "date": current_event.date,
        "start": current_event.start_time,
        "end": current_event.end_time,
        "text": current_event.text,
        "owner": current_event.member,
        "current_event": current_event,
        "prev_url": previous_url,
    })

@login_required
def event_delete(request, event_id):
    current_event = Event.objects.get(pk=event_id)

    current_event.delete()

    return HttpResponseRedirect(reverse("event:calendar"))

# @login_required
# def event_edit(request, event_id):
#     current_event = Event.objects.get(pk=event_id)
#     if request.method == "POST":
#         form = EventCreationFormSingle(request.POST)
#         if form.is_valid():
#             Event.objects.create(date=request.POST["date"], 
#                              start_time=request.POST["start_time"], 
#                              end_time=request.POST["end_time"], 
#                              text=request.POST["text"], 
#                              user=request.user,
#                              member=Member.objects.get(member_user=request.user),
#                              importance=request.POST["importance"],)
#             return HttpResponseRedirect(reverse("event:calendar"))
#     else:
#         form = EventCreationFormSingle()

#     return render(request, "event/eventadd.html", {
#         "form": form,
#     })


#########################################################################

@login_required
def calendar_to_pdf(request):
    day = datetime.today()
    year = day.year
    month = day.month

    year = int(year)
    month = int(month)

    cal = calendar.Calendar(6)                                          # 6, So sunday is the first. Maybe changed later.
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

    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="calendar.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    title = f"{calendar.month_name[month]} {year}"
    elements.append(Table([[title]], style=[
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
    ]))

    elements.append(Spacer(1, 20))

    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    table_data = [day_names]

    styles = getSampleStyleSheet()

    for week in days_in_month:
        row = []
        for day in week:
            if day == 0:  
                row.append("")
            else:
                count = len(row)
                cell_content = f"{day}\n"
                row.append(cell_content)
                for date, list in events_per_day.items():
                    for event in list:
                        if day == date:
                            start_time = event.start_time.strftime("%H:%M")
                            end_time = event.end_time.strftime("%H:%M")
                            text = event.text
                            old_text = row[count]
                            new_text = f"{old_text}\n{start_time} - {end_time}\n{text}"
                            row[count] = new_text
        table_data.append(row)
        
    # Create Table
    header_size = 50
    data_size = 100
    table = Table(table_data, colWidths=80, rowHeights= [header_size, data_size, data_size, data_size, data_size, data_size])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.crimson),
        # Table header
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'), 
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        # Table Data
        ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        
    ]))

    elements.append(table)
    doc.build(elements)

    return response

@login_required
def calendar_to_pdf_group(request, code):
    day = datetime.today()
    year = day.year
    month = day.month

    year = int(year)
    month = int(month)

    cal = calendar.Calendar(6)                                          # 6, So sunday is the first. Maybe changed later.
    days_in_month = cal.monthdayscalendar(year, month)

    current_group = Group.objects.get(group_code=code)

    current_join = Joining.objects.filter(joined_group = current_group).first().get_code()
    sorted_events = Event.objects.all().order_by("start_time")              # Sort event by time first
    all_events = sorted_events.filter(date__year=year, 
                                      date__month=month,)
    
    events_per_day = {}
    for event in all_events:
        day = event.date.day                    # get day of event date
        if day not in events_per_day:           # if this day isn't already in the list, 
            events_per_day[day] = []            # create list for that day

        current_event = event.member.joined_group.all()
        # print(event.member)
        # print(current_join)
        for item in current_event:
            #print(item.get_code())
            if item.get_code() == current_join:
                events_per_day[day].append(event) 


    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="calendar.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    title = f"{calendar.month_name[month]} {year}"
    elements.append(Table([[title]], style=[
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
    ]))

    elements.append(Spacer(1, 20))

    day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    table_data = [day_names]

    styles = getSampleStyleSheet()

    print(events_per_day)

    for week in days_in_month:
        row = []
        for day in week:
            if day == 0:  
                row.append("")
            else:
                count = len(row)
                cell_content = f"{day}\n"
                row.append(cell_content)
                for date, list in events_per_day.items():
                    for event in list:
                        if day == date:
                            start_time = event.start_time.strftime("%H:%M")
                            end_time = event.end_time.strftime("%H:%M")
                            text = event.text
                            old_text = row[count]
                            new_text = f"{old_text}\n{start_time} - {end_time}\n{text}"
                            row[count] = new_text
        table_data.append(row)
        
    # Create Table
    header_size = 50
    data_size = 100
    table = Table(table_data, colWidths=80, rowHeights= [header_size, data_size, data_size, data_size, data_size, data_size])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.crimson),
        # Table header
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'), 
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        # Table Data
        ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        
    ]))

    elements.append(table)
    doc.build(elements)

    return response