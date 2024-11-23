from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Group(models.Model):
    group_code = models.CharField(max_length=20) # Invite Code
    group_name = models.CharField(max_length=32) # Name
    group_slot = models.IntegerField(default=20) # Limit the amount of members
    
    def __str__(self):
        return f"{self.group_name}"
    
    def get_code(self):
        return f"{self.group_code}"

class Joining(models.Model):
    ranks_list = [
        ("owner", "Owner"),
        ("moderator", "Moderator"),
        ("member", "Member"),
    ]
    joined_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="join")       # Required, so Group can see Members
    joined_rank = models.CharField(choices=ranks_list, default="member", max_length=10)
                                                                                                
    def __str__(self):
        return f"{self.joined_group}"
    
    def get_code(self):
        return f"{self.joined_group.group_code}"
    
class Member(models.Model):
    member_code = models.CharField(max_length=20, blank=True)               # Exist if needed
    member_name = models.CharField(max_length=20)                           # Name
    member_user = models.ForeignKey(User, on_delete=models.CASCADE)      # Connect user to member
    member_info = models.CharField(max_length=128, blank=True)              # Free space to write stuff

    joined_group = models.ManyToManyField(Joining, blank=True, related_name="groups")

    def __str__(self):
        return f"{self.member_code} : {self.member_user}"