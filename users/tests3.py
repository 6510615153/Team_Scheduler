from django.test import TestCase
from .models import Member, Group, Joining
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.db.models import Subquery

class UsersTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='A69452048')
        self.user2 = User.objects.create_user(username='testuser2', password='B69452048')

        self.member = Member.objects.get(member_user=self.user1,)
        self.owner = Member.objects.get(member_user=self.user2,)

        self.group = Group.objects.create(group_code="gggg",
                                      group_name="testgroup",
                                      group_slot=20,)
        
        self.join1 = Joining.objects.create(joined_group=self.group)
        self.join2 = Joining.objects.create(joined_group=self.group, joined_rank="owner")

        self.member.joined_group.add(self.join1)
        self.owner.joined_group.add(self.join2)

        self.member.member_code = "testcode1"
        self.member.save()

        self.owner.member_code = "testcode2"
        self.owner.save()

    def test_confirm_page_available(self):
        """IF the page is available, return code 200"""
        response = self.client.get(reverse("users:confirm"))

        self.assertEqual(response.status_code,200)

    def test_correct_code_given(self):
        """If registration code is correct, context message should be listed as such."""
        code = {"code":'testcode1'}

        response = self.client.post(reverse('users:confirm'), code)

        self.assertEqual(response.context["message"], "Code successfully confirmed! Welcome!")

    def test_wrong_code_given(self):
        """If registration code is correct, context message should be listed as such."""
        code = {"code":'wrongcode1'}

        response = self.client.post(reverse('users:confirm'), code)

        self.assertEqual(response.context["message"], "Incorrect code.")