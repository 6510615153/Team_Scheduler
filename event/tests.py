from django.test import TestCase
from .models import Event
from .forms import EventCreationFormSingle
from users.models import Member, Joining, Group
from datetime import datetime, date, time
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

# Create your tests here.

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

    def test_correct_event_str(self):
        """String returned is correct"""

        self.client.force_login(self.user1)
        event_data = {
            "date": "2024-11-29",
            "start_time": "14:00",
            "end_time": "23:59",
            "text": "testevent",
            "importance": "1",
        }

        response = self.client.post(reverse("event:event_add"), event_data)
        event = Event.objects.first()

        self.assertEqual(str(event), "14:00:00")

    def test_end_time_before_error(self):
        """end time is before start time, error"""

        self.client.force_login(self.user1)
        event_data = {
            "date": "2024-11-29",
            "start_time": "23:59",
            "end_time": "14:00",
            "text": "testevent",
            "importance": "1",
        }

        form = EventCreationFormSingle(data=event_data)

        self.assertFalse(form.is_valid())

    def test_can_see_calendar(self):
        """Calendar is available to be seen"""

        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar'))
        self.assertEqual(response.status_code, 200)

    def test_can_see_calendar_group(self):
        """Calendar of Group is available to be seen"""

        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_group', args=("ffff",)))
        self.assertEqual(response.status_code, 200)

    def test_can_add_event(self):
        """You can add event"""
        self.client.force_login(self.user1)

        event_data = {
            "date": "2024-11-29",
            "start_time": "14:00",
            "end_time": "23:59",
            "text": "testevent",
            "importance": "1",
        }

        response = self.client.post(reverse("event:event_add"), event_data)

        event = Event.objects.first()
        self.assertIsNotNone(event)
        self.assertRedirects(response, reverse("event:calendar"))

    def test_form_is_gone_on_page_enter(self):
        """request isn't POST"""
        response = self.client.get(reverse('event:event_add'))
        
        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.context['form'], EventCreationFormSingle)

    def test_correct_variable_context_next_month_solo(self):
        """Check context next month"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change', args=[2024, 12]))

        self.assertEqual(response.context["next_month"], 1)
        self.assertEqual(response.context["next_year"], 2025)

    def test_correct_variable_context_prev_month_solo(self):
        """Check context prev month"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change', args=[2024, 1]))

        self.assertEqual(response.context["prev_month"], 12)
        self.assertEqual(response.context["prev_year"], 2023)

    def test_correct_variable_context_next_month_group(self):
        """Check context next month"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change_group', args=['ffff', 2024, 12]))

        self.assertEqual(response.context["next_month"], 1)
        self.assertEqual(response.context["next_year"], 2025)

    def test_correct_variable_context_prev_month_group(self):
        """Check context prev month"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change_group', args=['ffff', 2024, 1]))

        self.assertEqual(response.context["prev_month"], 12)
        self.assertEqual(response.context["prev_year"], 2023)

    # def test_correct_variable_context_prev_month_group(self):
    #     """Check context prev month"""
    #     self.client.force_login(self.user1)
    #     response = self.client.get(reverse('event:calendar_change_group', args=['ffff', 2024, 1]))

    #     self.assertEqual(response.context["prev_month"], 12)
    #     self.assertEqual(response.context["prev_year"], 2023)

    def test_member_join_correctly_gotten(self):
        """check member join correct"""

        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change_group', args=['ffff', 2024, 1]))

        current_group = Group.objects.get(group_code="ffff",)
        member_get_joined = self.member1.joined_group.all()

        current_join = Joining.objects.get(joined_group=current_group) 

        # self.member1.joined_group.add(self.join1)
        
        member_join = member_get_joined.get(joined_group=current_group)

        self.assertEqual(member_join, current_join)

    def test_member_join_not_exist(self):
        """check member join not exist"""

        self.member1.joined_group.remove(self.join1)

        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:calendar_change_group', args=['ffff', 2024, 1]))

        current_group = Group.objects.get(group_code="ffff",)
        member_get_joined = self.member1.joined_group.all()

        current_join = Joining.objects.get(joined_group=current_group) 
        
        if not member_get_joined.exists():
            member_join = Member.objects.get(member_user=self.user1)


        self.assertNotEqual(member_join, current_join)

    def test_event_loop(self):
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
        
        self.assertEqual(len(events_per_day[23]), 1)