from django.urls import path
from . import views

app_name = "event"

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),  
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_change'),

    path('calendar/event_add/', views.event_add, name='event_add'),
    path('calendar/event_delete/<int:event_id>', views.event_delete, name='event_delete'),

    path('<str:code>/calendar/', views.calendar_view_group, name='calendar_group'),  
    path('<str:code>/calendar/<int:year>/<int:month>/', views.calendar_view_group, name='calendar_change_group'),

    path('calendar/<int:event_id>/', views.see_event_detail, name='event_detail'),

    path('calendar/create_pdf/<int:rcv_year>/<int:rcv_month>', views.calendar_to_pdf, name='calendar_pdf'),
    path('<str:code>/calendar/create_pdf/<int:rcv_year>/<int:rcv_month>', views.calendar_to_pdf_group, name='calendar_pdf_group'),
]