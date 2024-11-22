from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('dashboard', views.index, name='dashboard'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),

    path('group_view', views.group_view, name='group_view'),
    path('group_create', views.group_create, name='group_create'),

    path('join', views.join_group, name='join_group'),
    path('group_view/<str:code>', views.see_group_page, name='see_group')
]