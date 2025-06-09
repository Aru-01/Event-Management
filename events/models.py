from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# class Participant(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     events = models.ManyToManyField("Event", related_name="participants")

#     def __str__(self):
#         return self.name


class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    img = models.ImageField(
        upload_to="event-img/", blank=True, null=True, default="event-img/no.png"
    )
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="events"
    )
    participants = models.ManyToManyField(
        User, related_name="joined_events", blank=True, null=True
    )

    def __str__(self):
        return self.name
