from django.test import TestCase
from .models import Event
from users.models import Member, Joining, Group
from datetime import date, time
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Subquery

class EventTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='testuser1', password='A69452048')
        self.user2 = User.objects.create(username='testuser2', password='B69452048')

        self.member1 = Member.objects.get(member_user=self.user1,)
        
        self.member2 = Member.objects.get(member_user=self.user2,)
        
        self.group1 = Group.objects.create(group_code="ffff",
                                      group_name="testgroup",
                                      group_slot=20,)

        self.join1 = Joining.objects.create(joined_group=self.group1)
    
        self.member1.joined_group.add(self.join1)

        self.event1 = Event.objects.create(
            date=date(2024,11,23),
            start_time=time(14, 0),
            end_time=time(23, 59),
            text="event1",
            user=self.user1,
            member=self.member1,
        )

        self.event2 = Event.objects.create(
            date=date(2024,11,24),
            start_time=time(14, 0),
            end_time=time(23, 59),
            text="event2",
            user=self.user2,
            member=self.member2,
        )

    def test_event_loop_group(self):
        """check if event loop work"""

        event1 = Event.objects.create(
            date=date(2024,11,23),
            start_time=time(14, 0),
            end_time=time(23, 59),
            text="event1",
            user=self.user1,
            member=self.member1,
        )
        event2 = Event.objects.create(
            date=date(2024,11,24),
            start_time=time(7, 0),
            end_time=time(23, 59),
            text="event2",
            user=self.user2,
            member=self.member2,
        )

        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change_group', args=['ffff', 2024, 11]))

        current_group = Group.objects.get(group_code="ffff")

        current_join = Joining.objects.filter(joined_group = current_group).first().get_code()
        sorted_events = Event.objects.all().order_by("start_time")              # Sort event by time first
        all_events = sorted_events.filter(date__year=2024, 
                                      date__month=11,)

        events_per_day = {}
        for event in all_events:
            day = event.date.day                    # get day of event date
            if day not in events_per_day:           # if this day isn't already in the list, 
                events_per_day[day] = []            # create list for that day

            current_event = event.member.joined_group.all()
            for item in current_event:
                #print(item.get_code())
                if item.get_code() == current_join:
                    events_per_day[day].append(event) 
        
        self.assertEqual(events_per_day[23], response.context["events"][23])

    def test_event_loop_single(self):
        """check if event loop work"""

        event1 = Event.objects.create(
            date=date(2024,11,23),
            start_time=time(14, 0),
            end_time=time(23, 59),
            text="event1",
            user=self.user1,
            member=self.member1,
        )
        event2 = Event.objects.create(
            date=date(2024,11,24),
            start_time=time(7, 0),
            end_time=time(23, 59),
            text="event2",
            user=self.user2,
            member=self.member2,
        )

        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change', args=[2024, 11]))

        sorted_events = Event.objects.all().order_by("start_time")              # Sort event by time first
        all_events = sorted_events.filter(date__year=2024, 
                                      date__month=11,)

        events_per_day = {}
        for event in all_events: 
            day = event.date.day                    # get day of event date 
            if day not in events_per_day:           # if this day isn't already in the list,  
                events_per_day[day] = []            # create list for that day 
            events_per_day[day].append(event)       # add event into that day 
        
        self.assertEqual(events_per_day[23], response.context["events"][23])
    
    