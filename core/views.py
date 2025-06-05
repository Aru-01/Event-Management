from django.shortcuts import render
from events.models import Event


# Create your views here.
def home(request):
    events = Event.objects.all()[:4]
    return render(request, "Home/home.html", {"events": events})


def contact(request):
    return render(request, "Contact/contact.html")
