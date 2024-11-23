from django.test import TestCase
from .models import Event
from .forms import EventCreationFormSingle
from users.models import Member, Joining, Group
from datetime import datetime, date, time
from django.contrib.auth.models import User
from django.urls import reverse
from . import views

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

    def test_event_detail_available(self):
        """If available, should return code 200"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('event:event_detail', args=(self.event1.id,)))
        self.assertEqual(response.status_code, 200)

    def test_working_pdf(self):
        """If PDF is created, response content type should be PDF, and 'calendar.pdf' should be in Content-Disposition section"""
        self.client.force_login(self.user1)

        response = self.client.get(reverse('event:calendar_pdf'))

        self.assertEqual(response['Content-Type'], 'application/pdf')

        self.assertIn('calendar.pdf', response['Content-Disposition'])

    def test_event_delete_success(self):
        """Event is successfully deleted after deleting. (== None) and REDIRECT SUCCESS"""
        self.client.force_login(self.user1)

        response = self.client.get(reverse('event:event_delete', args=(self.event1.id, )))

        self.assertEqual(Event.objects.filter(pk=1).first(), None)

        self.assertEqual(response.status_code, 302)

        