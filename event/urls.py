from django.urls import path
from . import views

app_name = "event"

urlpatterns = [
    path('event/', views.index, name='index'),
    path('calendar/', views.calendar_view, name='calendar'),  
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_change'),

    path('calendar/eventadd', views.event_add, name='event_add'),

    path('<str:code>/calendar/', views.calendar_view_group, name='calendar_group'),  
    path('<str:code>/calendar/<int:year>/<int:month>/', views.calendar_view_group, name='calendar_change_group'),
]