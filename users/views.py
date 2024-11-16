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
            return HttpResponseRedirect(reverse("users:dashboard"))
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
    member = Member.objects.get(member_user=request.user)
    joined = member.joined_group.all()
    groups = Group.objects.filter(join__in=member.joined_group.all())
    group_codes = groups.values_list('group_code', flat=True)
    group_dict = dict(zip(joined, group_codes))
    print(joined)
    print(group_codes)
    print(dict(zip(joined, group_codes)))
    return render(request, "users/group_view.html", {
        "groups": joined,
        "member": member,
        "group_dict": group_dict,
    })

def group_create(request):
    member = Member.objects.get(member_user=request.user)
    if request.method == "POST":
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save()
            joined = Joining.objects.create(joined_group=group)
            member.joined_group.add(joined)
            return HttpResponseRedirect(reverse("users:group_view"))
    else:
        form = GroupCreationForm()

    return render(request, "users/group_create.html", {
        "form": form,
    })

def group_page(request):
    pass

def join_group(request):
    member = Member.objects.get(member_user=request.user)
    if request.method == "POST":
        code = request.POST["group_code"]
        group = Group.objects.get(group_code=code)
        joined = Joining.objects.get(joined_group=group)
        member.joined_group.add(joined)
        return HttpResponseRedirect(reverse("users:group_view"))