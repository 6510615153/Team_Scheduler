from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
    member_code = models.CharField(max_length=20, blank=True)               # Exist if needed
    member_name = models.CharField(max_length=20)                           # Name
    member_user = models.OneToOneField(User, on_delete=models.CASCADE)      # Connect user to member
    member_info = models.CharField(max_length=128, blank=True)              # Free space to write stuff

    # To see how many group you've joined
    # the schedule table of another person
    # REQUIRE schedule models

    # time_table = models.............
    # schedule = models...................

    def __str__(self):
        return f"{self.member_code} : {self.member_user}"
    
class Joining(models.Model):
    joined_user = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="join")       # Required, so Group can see Members
                                                                                                # Member can see groups
    def __str__(self):
        return f"{self.joined_user}"

class Group(models.Model):
    group_code = models.CharField(max_length=20) # Invite Code
    group_name = models.CharField(max_length=32) # Name
    group_slot = 20 # Limit the amount of members

    group_members = models.ManyToManyField(Joining, blank=True, related_name="groups")
    
    def __str__(self):
        return f"{self.group_code} : {self.group_name} total_slot: {self.group_slot}"
    
    def countMember(self):
        return self.group_members.count()

    def memberExceedLimit(self):
        if self.group_members.count() >= self.group_slot:
            return True
        return False
