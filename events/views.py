from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event, Category
from events.forms import EventModelForm, CategoryForm, ParticipantForm
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, "Home/home.html")


def events(request):
    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    events = (
        Event.objects.select_related("category").prefetch_related("participants").all()
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


def contact(request):
    return render(request, "Contact/contact.html")


def dashboard(request):
    return render(request, "Dashboard/dashboard.html")


def create_event(request):
    form = EventModelForm()

    if request.method == "POST":
        form = EventModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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
            return redirect("create_event")
        else:
            messages.error(request, "Something Went wrong.")
    else:
        form = CategoryForm()
    context = {"category_form": form}
    return render(request, "Dashboard/add_category/add_category.html", context)


def add_participant(request):
    form = ParticipantForm()
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant added successfully!")
            return redirect("create_event")
        else:
            messages.error(request, "Something Went wrong.")
    else:
        form = ParticipantForm()
    context = {"participant_form": form}
    return render(request, "Dashboard/add_participant/add_participant.html", context)
