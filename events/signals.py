from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from events.models import Event
from django.conf import settings
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Event.participants.through)
def notify_rsvp_event(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = instance.participants.get(pk=user_id)
            subject = f"🎉 RSVP Confirmation for {instance.name}"
            message = (
                f"Hi {user.first_name},\n\n"
                f'You\'ve successfully RSVPed for the event "{instance.name}"!\n\n'
                f"📍 Location: {instance.location}\n"
                f"📅 Date: {instance.date}\n\n"
                "Thank you for joining. We look forward to seeing you there!\n\n"
                "Cheers,\nThe E-Management Team 🎈"
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                )
            except Exception as e:
                print(f"❌ Failed to send RSVP email to {user.email}: {str(e)}")
