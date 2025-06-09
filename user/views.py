from django.shortcuts import render, redirect, HttpResponse
from user.forms import CustomRegisterForm, CreateGroupForm, ChangeRoleForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch
from events.models import Event, Category
from django.db.models import Q, Count
from django.utils.timezone import localtime

# Create your views here.


def sign_up(request):
    if request.method == "GET":
        form = CustomRegisterForm()
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            print("\n\n\n", form.cleaned_data)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password1"))
            user.is_active = False
            user.save()
            messages.success(
                request, "A activation Mail Send your mail. Plase check..."
            )
            return redirect("sign-in")
    return render(request, "sign-up/sign_up.html", {"form": form})


def activate_user(reqest, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("User Not Found.!")


def sign_in(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "sign-in/sign_in.html", {"form": form})


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")


def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch("groups", queryset=Group.objects.all(), to_attr="all_groups")
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No Group Assigned"
    return render(request, "admin/admin_dashboard.html", {"users": users})


def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    return render(request, "admin/Group-list/group_list.html", {"groups": groups})


def event_dashboard(request):
    event_type = request.GET.get("type", "today")

    base_query = Event.objects.select_related("category").prefetch_related(
        "participants"
    )

    today = localtime().date()
    print("\n\n", today, "\n\n")
    if event_type == "upcoming":
        events = base_query.filter(date__gt=today)
    elif event_type == "past":
        events = base_query.filter(date__lt=today)
    elif event_type == "today":
        events = base_query.filter(date=today)
    else:
        events = base_query

    counts = Event.objects.aggregate(
        total=Count("id"),
        upcoming=Count("id", filter=Q(date__gt=today)),
        past=Count("id", filter=Q(date__lt=today)),
        today=Count("id", filter=Q(date=today)),
    )

    total_participants = (
        User.objects.filter(joined_events__isnull=False).distinct().count()
    )
    total_categories = Category.objects.count()

    context = {
        "events": events,
        "counts": counts,
        "total_participants": total_participants,
        "total_categories": total_categories,
        "event_type": event_type,
    }

    return render(request, "admin/event-Dashboard/event_dashboard.html", context)


def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created sucessfuly")
            return redirect("group-list")
    return render(request, "admin/create_group/create_group.html", {"form": form})


def change_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = ChangeRoleForm()
    if request.method == "POST":
        form = ChangeRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear()
            user.groups.add(role)
            messages.success(
                request, f"user {user.username} has been assigned to the {role} role"
            )
            return redirect("admin-dashboard")

    return render(
        request, "admin/Change_role/change_role.html", {"form": form, "user": user}
    )


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "user remove successfully")
        return redirect("admin-dashboard")

    messages.warning(request, "Invalid...")
    return redirect("admin-dashboard")
