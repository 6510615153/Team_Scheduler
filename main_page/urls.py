from django.urls import path
from . import views

app_name = "main_page"

urlpatterns = [
    path("", views.main_page, name='index_main'),
    path("about", views.about, name='about'),
]