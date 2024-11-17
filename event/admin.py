from django.contrib import admin
from .models import Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'end_time', 'text', 'member']

# class EventGroupAdmin(admin.ModelAdmin):
#     list_display = ['date', 'start_time', 'end_time', 'text', 'group']

admin.site.register(Event, EventAdmin)