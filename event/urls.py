from django.urls import path
from . import views

app_name = "event"

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar_view, name='calendar'),  
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_change'),
    path('calendar/eventadd', views.event_add, name='event_add'),
]