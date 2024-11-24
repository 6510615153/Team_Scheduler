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

    def test_join_group_not_exist(self):
        """Join group fail, render page with message context"""
        self.client.force_login(self.user1)

        group_data = {
            "group_code": "WRONG",
        }

        response = self.client.post(reverse("users:join_group"), group_data)

        self.assertEqual(response.context["message"], "The group does not exist.")

    def test_join_group_full(self):
        """Join group fail, render page with message context"""
        self.client.force_login(self.user1)

        self.group.group_slot = 0;
        self.group.save()

        group_data = {
            "group_code": "gggg",
        }

        response = self.client.post(reverse("users:join_group"), group_data)

        self.assertEqual(response.context["message"], "Max Member reached.")

    def test_leave_group_member(self):
        """leave group successful should redirect. Code 302"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse("users:leave_group", args=['gggg']))

        self.assertEqual(response.status_code, 302)

    def test_leave_group_owner(self):
        """leave group AS OWNER should REMOVE GROUP. Check to see if group is deleted."""
        self.client.force_login(self.user2)
        response = self.client.get(reverse("users:leave_group", args=['gggg']))

        self.assertEqual(Group.objects.filter(group_code="gggg").first(), None)

    def test_see_group_page(self):
        """If group page is available, code 200"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse("users:see_group", args=['gggg']))

        self.assertEqual(response.status_code,200)

    def test_correct_context_group_page(self):
        """Context should be correct for the group page."""
        self.client.force_login(self.user1)
        response = self.client.get(reverse("users:see_group", args=['gggg']))

        joined = Joining.objects.filter(joined_group=self.group)
        member_joined = Member.objects.filter(joined_group__in=Subquery(joined.values('id')))
        total_joined = member_joined.count()

        self.assertEqual(response.context["group"], self.group)
        self.assertEqual(response.context["total_member"], total_joined)
        self.assertEqual(response.context["owner"], self.owner.member_name)
