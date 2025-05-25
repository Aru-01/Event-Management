from django.urls import path
from events.views import (
    events,
    contact,
    dashboard,
    create_event,
    add_category,
    add_participant,
)

urlpatterns = [
    path("events/", events, name="events"),
    path("contact-us/", contact, name="contact-us"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create-event/", create_event, name="create_event"),
    path("add-category/", add_category, name="add_category"),
    path("add-participant/", add_participant, name="add_participant"),
]
