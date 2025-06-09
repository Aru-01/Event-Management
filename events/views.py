from django.shortcuts import render, redirect, HttpResponse
from events.models import Event, Category
from events.forms import CategoryForm, EventModelForm
from django.contrib import messages
from django.db.models import Q, Count
from django.utils.timezone import localtime
from django.contrib.auth.models import User


# Create your views here.


def events(request):
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    events = (
        Event.objects.select_related("category")
        .prefetch_related("participants")
        .order_by("-date")
    )

    if search:
        events = events.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(location__icontains=search)
        )

    if category:
        events = events.filter(category__name__icontains=category)

    if date_from:
        events = events.filter(date__gte=date_from)

    if date_to:
        events = events.filter(date__lte=date_to)

    categories = Category.objects.values_list("name", flat=True)

    context = {
        "events": events,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "date_from": date_from,
        "date_to": date_to,
    }
    return render(request, "Events/events.html", context)


def dashboard(request):
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

    return render(request, "Dashboard/dashboard.html", context)


def create_event(request):
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            participants = form.cleaned_data.get("participants")
            if participants:
                event.participants.set(participants)

            messages.success(request, "Event created successfully!")
            return redirect("events")
    context = {"form": form}
    return render(request, "Create_event/create_event.html", context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect("Total_Categories")
        else:
            messages.error(request, "Something Went wrong.")
    else:
        form = CategoryForm()
    context = {"category_form": form}
    return render(request, "Dashboard/add_category/add_category.html", context)


def delete_participant(request, id):
    if request.method == "POST":
        try:
            participant = User.objects.get(id=id)
            participant.delete()
        except User.DoesNotExist:
            print(f"User does not exist.")
        return redirect("Total_Participants")
    else:
        return redirect("Total_Participants")


def Total_Participants(request):
    pass
    participants = User.objects.filter(joined_events__isnull=False).distinct()

    return render(
        request,
        "Dashboard/Total_Participants/Total_Participants.html",
        {"participants": participants},
    )


def Total_Categories(request):
    categories = Category.objects.all()
    return render(
        request,
        "Dashboard/Total_Categories/Total_Categories.html",
        {"categories": categories},
    )


def delete_category(request, id):
    if request.method == "POST":
        # print("\n\n", id, "\n\n")
        category = Category.objects.get(id=id)
        category.delete()
        return redirect("Total_Categories")
    else:
        return redirect("Total_Categories")


def event_details(request, id):
    event = (
        Event.objects.select_related("category")
        .prefetch_related("participants")
        .get(id=id)
    )
    participants = event.participants.all()
    context = {"event": event, "participants": participants}
    return render(request, "shared/event_details.html", context)


def delete_event(request, id):
    if request.method == "POST":
        # print("\n\n", id, "\n\n")
        event = Event.objects.get(id=id)
        event.delete()
        return redirect("events")
    else:
        return redirect("events")


def update_event(request, id):
    event = Event.objects.get(id=id)
    form = EventModelForm(instance=event)
    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES, instance=event)
        # print(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            if "img" in request.FILES:
                event.img = request.FILES["img"]
            else:
                event.img = event.img
            event.save()
            participants = form.cleaned_data.get("participants")
            if participants:
                event.participants.set(participants)

            messages.success(request, "Event created successfully!")
            return redirect("events")
    context = {"form": form}
    return render(request, "Create_event/create_event.html", context)


def rsvp_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        user = request.user
        event.participants.add(user)
        messages.success(request, f"You have successfully RSVPed to '{event.name}'!")

        return redirect("event_details", id=id)


def rsvp_dashboard(request):
    joined_events = (
        request.user.joined_events.select_related("category").all().order_by("-date")
    )
    context = {
        "joined_events": joined_events,
    }
    return render(request, "rsvp_dashboard/rsvp_dashboard.html", context)
