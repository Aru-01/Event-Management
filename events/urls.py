from django.urls import path
from events.views import (
    events,
    dashboard,
    create_event,
    add_category,
    Total_Participants,
    delete_participant,
    Total_Categories,
    delete_category,
    event_details,
    delete_event,
    update_event,
    rsvp_event,
    rsvp_dashboard,
)

urlpatterns = [
    path("events/", events, name="events"),
    path("dashboard/", dashboard, name="dashboard"),
    path("rsvp_dashboard/", rsvp_dashboard, name="rsvp_dashboard"),
    path("create-event/", create_event, name="create_event"),
    path("add-category/", add_category, name="add_category"),
    path(
        "dashboard/Total-Participants/", Total_Participants, name="Total_Participants"
    ),
    path(
        "dashboard/Total-Participants/<int:id>",
        delete_participant,
        name="delete_participant",
    ),
    path("dashboard/Total_Categories/", Total_Categories, name="Total_Categories"),
    path(
        "dashboard/Total_Categories/<int:id>", delete_category, name="delete_category"
    ),
    path("event-details/<int:id>/", event_details, name="event_details"),
    path("event-details/delete/<int:id>/", delete_event, name="delete_event"),
    path("event-details/rsvp/<int:id>/", rsvp_event, name="rsvp_event"),
    path("update-event/<int:id>/", update_event, name="update_event"),
]
