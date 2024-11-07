from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def main_page(request):
    return render(request, "main_page/main_page.html")

def about(request):
    return render(request, "main_page/about.html")