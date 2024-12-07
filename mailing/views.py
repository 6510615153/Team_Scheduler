from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def build_mail(rcv_subject, rcv_message, rcv_email):

    subject = rcv_subject

    message = rcv_message

    from_email = settings.EMAIL_HOST_USER

    to_email = rcv_email

    send_mail(subject, message, from_email, to_email)   

# def send(request):
#     build_mail()
#     HttpResponseRedirect(reverse("users:dashboard"))

def send(rcv_subject, rcv_message, rcv_email):
    build_mail(rcv_subject, rcv_message, rcv_email)