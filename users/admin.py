from django.contrib import admin
from .models import Member, Group, Joining

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "member_code", "member_name")

class GroupAdmin(admin.ModelAdmin):
    list_display = ("group_code", "group_name", "group_slot")

# admin.site.register(GroupJoining)
admin.site.register(Group, GroupAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Joining)