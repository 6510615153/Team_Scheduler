from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, GroupCreationForm
from django.contrib.auth.decorators import login_required
from .models import Group, Member, Joining
from django.db.models import Subquery
from django.contrib import messages

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
            group = form.save()
            joined_mem = Joining.objects.create(joined_group=group, joined_rank="member")
            joined_own = Joining.objects.create(joined_group=group, joined_rank="owner")
            member.joined_group.add(joined_own)
            return HttpResponseRedirect(reverse("users:group_view"))
    else:
        form = GroupCreationForm()

    return render(request, "users/group_create.html", {
        "form": form,
    })

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