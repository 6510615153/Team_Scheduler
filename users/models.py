from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    group_code = models.CharField(max_length=20) # Invite Code
    group_name = models.CharField(max_length=32) # Name
    group_slot = models.IntegerField(default=20) # Limit the amount of members
    
    def __str__(self):
        return f"{self.group_name}"

class Joining(models.Model):
    joined_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="join")       # Required, so Group can see Members
                                                                                                 # Member can see groups
    def __str__(self):
        return f"{self.joined_group}"
    
class Member(models.Model):
    member_code = models.CharField(max_length=20, blank=True)               # Exist if needed
    member_name = models.CharField(max_length=20)                           # Name
    member_user = models.ForeignKey(User, on_delete=models.CASCADE)      # Connect user to member
    member_info = models.CharField(max_length=128, blank=True)              # Free space to write stuff

    joined_group = models.ManyToManyField(Joining, blank=True, related_name="groups")
    
    # To see how many group you've joined
    # the schedule table of another person
    # REQUIRE schedule models

    # time_table = models.............
    # schedule = models...................

    def __str__(self):
        return f"{self.member_code} : {self.member_user}"