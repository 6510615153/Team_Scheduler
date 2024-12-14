from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, GroupCreationForm
from django.contrib.auth.decorators import login_required
from .models import Group, Member, Joining
from django.db.models import Subquery
from django.contrib.auth.models import User

import secrets
from django.conf import settings
from mailing.views import send

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

        if user is None:
            return render(request, "users/login.html", {
                "Message" : "Wrong Username or Password."
            })
        else:
            login(request, user)
            return HttpResponseRedirect(reverse("users:dashboard"))
        
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "Message" : "Logged out."
    })

def code_generate_member():
    while True:
        member_code = secrets.token_hex(8)
        if not Member.objects.filter(member_code=member_code).exists():
            return member_code

def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            code = code_generate_member()
            member = Member.objects.get(member_user=user)

            member.member_code = code
            member.save()

            subject = "Please confirm your Registeration"
            message = f"Your registeration confirmation code is : {code}"
            to_email = []
            to_email.append(user.email)

            send(subject, message, to_email)   

            return HttpResponseRedirect(reverse("users:confirm"))
    else:
        form = UserRegisterForm()

    return render(request, "users/register.html", {
        "form": form,
        "Message" : "Register your account to gain access.",
    })

def confirm(request):
    if request.method == "POST":
        code = request.POST["code"]

        member = Member.objects.filter(member_code=code).first()

        if member is not None:
            user = member.member_user
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, "users/index.html", {
                "message": "Code successfully confirmed! Welcome!",
            })
        
        else:
            return render(request, "users/confirm.html", {
                "message": "Incorrect code.",
            })
        
    return render(request, "users/confirm.html")

@login_required
def group_view(request):
    member = Member.objects.get(member_user=request.user)
    joined = member.joined_group.all()
    groups = Group.objects.filter(join__in=member.joined_group.all())
    group_codes = groups.values_list('group_code', flat=True)
    group_dict = dict(zip(joined, group_codes))
    return render(request, "users/group_view.html", {
        "groups": joined,
        "member": member,
        "group_dict": group_dict,
    })

@login_required
def group_create(request):
    member = Member.objects.get(member_user=request.user)
    if request.method == "POST":
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.group_code = code_generate_group()  
            group.save()  

            joined_mem = Joining.objects.create(joined_group=group, joined_rank="member")
            joined_own = Joining.objects.create(joined_group=group, joined_rank="owner")
            member.joined_group.add(joined_own)
            return HttpResponseRedirect(reverse("users:group_view"))
    else:
        form = GroupCreationForm()

    return render(request, "users/group_create.html", {
        "form": form,
    })

def code_generate_group():
    while True:
        group_code = secrets.token_hex(8)
        if not Group.objects.filter(group_code=group_code).exists():
            return group_code

@login_required
def join_group(request):
    member = Member.objects.get(member_user=request.user)
    joined = member.joined_group.all()
    groups = Group.objects.filter(join__in=member.joined_group.all())
    group_codes = groups.values_list('group_code', flat=True)
    group_dict = dict(zip(joined, group_codes))
    if request.method == "POST":
        code = request.POST["group_code"]
        current_group = Group.objects.filter(group_code=code).first()
        if current_group is None:
            return render(request, 'users/group_view.html', {     
                "message": "The group does not exist.",
                "groups": joined,
                "member": member,
                "group_dict": group_dict,
            })
        else:
            joined = Joining.objects.filter(joined_group=current_group)
            member_joined = Member.objects.filter(joined_group__in=Subquery(joined.values('id')))
            total_joined = member_joined.count()
        
            if total_joined >= current_group.group_slot:
                return render(request, 'users/group_view.html', {     
                    "message": "Max Member reached.",
                    "groups": joined,
                    "member": member,
                    "group_dict": group_dict,
                })
            else:
                group = Group.objects.get(group_code=code)
                joined = Joining.objects.get(joined_group=group, joined_rank="member")
                member.joined_group.add(joined)
                return HttpResponseRedirect(reverse("users:group_view"))
    
@login_required
def leave_group(request, code):
    member = Member.objects.get(member_user=request.user)
    group = Group.objects.get(group_code=code)
    joined = member.joined_group.get(joined_group=group)
    member.joined_group.remove(joined)

    if joined.joined_rank == "owner":
        group.delete()

    return HttpResponseRedirect(reverse("users:group_view"))
    
@login_required
def see_group_page(request, code):
    current_group = Group.objects.get(group_code=code)
    joined = Joining.objects.filter(joined_group=current_group)
    member_joined = Member.objects.filter(joined_group__in=Subquery(joined.values('id')))
    
    total_joined = member_joined.count()

    owner = ""
    for member in member_joined:
        current_joined = member.joined_group.get(joined_group=current_group)
        if current_joined.joined_rank == "owner":
            owner = member.member_name
            break

    return render(request, 'users/group_page.html', {     
        "group": current_group,
        "code": current_group.group_code,
        "name": current_group.group_name,
        "slot": current_group.group_slot,
        "total_member": total_joined,
        "owner": owner
    })