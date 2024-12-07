from django.urls import path
from . import views

app_name = "mailing"

urlpatterns = [
    path('send/', views.send, name='send'),  
]