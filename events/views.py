from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.models import Event
from events.forms import EventModelForm, CategoryForm, ParticipantForm
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, "Home/home.html")


def events(request):
    events = (
        Event.objects.select_related("category").prefetch_related("participants").all()
    )
    # print("\n\n", events, "\n\n")
    context = {
        "events": events,
    }
    return render(request, "Events/events.html", context)


def contact(request):
    return render(request, "Contact/contact.html")


def dashborad(request):
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
            return redirect("dashborad")
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
            return redirect("dashborad")
        else:
            messages.error(request, "Something Went wrong.")
    else:
        form = ParticipantForm()
    context = {"participant_form": form}
    return render(request, "Dashboard/add_participant/add_participant.html", context)
