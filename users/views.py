from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, GroupCreationForm
from django.contrib.auth.decorators import login_required
from .models import Group, Member, Joining

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))
    return render(request, "users/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, "users/login.html", {
                "Message" : "Wrong Username or Password."
            })
        
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "Message" : "Logged out."
    })

def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "users/login.html", {
                "Message" : "You've successfully registered!",
            })
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {
        "form": form,
        "Message" : "Register your account to gain access.",
    })

def group_view(request):
    groups = Group.objects.all()
    member = Member.objects.get(member_user=request.user)
    joined = member.joined_group.all()
    return render(request, "users/group_list.html", {
        "groups": joined,
        "member": member,
    })

def group_create(request):
    member = Member.objects.get(member_user=request.user)
    if request.method == "POST":
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save()
            joined = Joining.objects.create(joined_group=group)
            member.joined_group.add(joined)
            return HttpResponseRedirect(reverse("users:group"))
    else:
        form = GroupCreationForm()

    return render(request, "users/group_create.html", {
        "form": form,
    })

def group_page(request):
    pass