from django.test import TestCase
from .models import Member, Group, Joining
from .forms import GroupCreationForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login

# Create your tests here.

class UsersTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='A69452048')

        self.member = Member.objects.get(member_user=self.user,)

        self.group = Group.objects.create(group_code="gggg",
                                      group_name="testgroup",
                                      group_slot=20,)
        
        self.join = Joining.objects.create(joined_group=self.group)

    def test_joining_str(self):
        self.assertEqual(str(self.join), "testgroup")

    def test_joining_code(self):
        self.assertEqual(self.join.get_code(), "gggg")

    def test_group_str(self):
        self.assertEqual(str(self.group), "testgroup")

    def test_group_code(self):
        self.assertEqual(self.group.get_code(), "gggg")

    def test_member_str(self):
        self.assertEqual(str(self.member), "testuser1")


    #####################################################################

    def test_dashboard_unavailable(self):
        """Redirect to login first"""
        
        response = self.client.post(reverse('users:dashboard'))

        self.assertEqual(response.status_code, 302)  

    def test_dashboard_available(self):
        """Dashboard is available, code 200"""
        self.client.force_login(self.user)

        response = self.client.get(reverse('users:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_available(self):
        """Login Page available"""

        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Logout show login page, code 200"""

        response = self.client.get(reverse('users:logout'))

        self.assertEqual(response.status_code, 200)

    def test_login_form_correct(self):
        """Success will give code 200"""

        credentials = {"username":'testuser1', 
                    "password":'A69452048'}

        response = self.client.post(reverse('users:login'), credentials)

        self.assertEqual(response.status_code, 302)

    # def test_redirect_after_login(self):
    #     """Already logged in will redirect"""
    #     self.client.force_login(self.user)
        
    #     response = self.client.post(reverse('users:login'))

    #     self.assertEqual(response.status_code, 302)  
        
    def test_login_fail(self):
        """Wrong password, render login again, code 200"""

        credentials = {"username":'testuser1', 
                    "password":'asdasdasdasdasdsd'}

        response = self.client.post(reverse('users:login'), credentials)

        self.assertEqual(response.status_code, 200)

    def test_register_page_available(self):
        """Page shows up. Code 200"""

        response = self.client.get(reverse("users:register"))

        self.assertEqual(response.status_code, 200)

    def test_can_register(self):
        """You can register, it should render login page, 200"""

        register_data = {
            "username": "testuser3",
            "email": "testuser@example.com",
            "password1": "C69452048",
            "password2": "C69452048",
        }

        response = self.client.post(reverse("users:register"), register_data)

        self.assertEqual(response.status_code, 302)

    def test_group_view_available(self):
        """You can view available group, code 200"""

        self.client.force_login(self.user)
        # member = Member.objects.get(member_user=request.user) 
        # joined = member.joined_group.all() 
        # groups = Group.objects.filter(join__in=member.joined_group.all()) 
        # group_codes = groups.values_list('group_code', flat=True) 
        # group_dict = dict(zip(joined, group_codes)) 

        response = self.client.get(reverse("users:group_view"))

        self.assertEqual(response.status_code, 200)

    def test_can_create_group(self):
        """You can create group, it should redirect to group view, 302"""
        self.client.force_login(self.user)

        group_data = {
            "group_code": "ffff",
            "group_name": "asdfgg",
        }

        response = self.client.post(reverse("users:group_create"), group_data)

        self.assertEqual(response.status_code, 302)

    def test_form_is_gone_on_page_enter_group(self):
        """request isn't POST, render page code 200"""
        self.client.force_login(self.user)

        response = self.client.get(reverse('users:group_create'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], GroupCreationForm)

    def test_join_group_success(self):
        """Join group success, redirect"""
        self.client.force_login(self.user)

        group_data = {
            "group_code": "gggg",
        }

        response = self.client.post(reverse("users:join_group"), group_data)

        self.assertEqual(response.status_code, 302)