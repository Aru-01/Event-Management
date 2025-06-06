from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail


@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = (
            f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        )
        subject = "🎉 Welcome to E-Management – Activate Your Account Now!"
        message = (
            f"Hi {instance.username}, 👋\n\n"
            "Welcome to E-Management – where amazing events come to life! 🎪✨\n\n"
            f"Please activate your account by clicking the link below:\n{activation_url}\n\n"
            "Once you're in, you'll be able to:\n"
            "✅ Discover trending events\n"
            "✅ Book unforgettable experiences\n"
            "✅ Create and manage your own events\n\n"
            "If you didn’t sign up for this, no worries – just ignore this email.\n\n"
            "Cheers,\n"
            "The E-Management Team 🎈\n"
            f"Need help? Reach us at {settings.EMAIL_HOST_USER}"
        )
        recipient_list = [instance.email]
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
            )
        except Exception as e:
            print(f"Failed to send mail {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def Assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name="Participant")
        instance.groups.add(user_group)
        instance.save()


@receiver(m2m_changed, sender=User.groups.through)
def notify_user_role_change(sender, instance, action, **kwargs):
    if action == "post_add":
        group_names = [group.name for group in instance.groups.all()]
        subject = "Your Role Has Been Updated"
        message = (
            f"Hi {instance.first_name or instance.username},\n\n"
            f"Your role has been updated.\n"
            f"Current role(s): {', '.join(group_names)}\n\n"
            "If you have any questions, feel free to contact us.\n\n"
            "Thank you,\nE Management Team"
        )
        recipient_list = [instance.email]

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
        )
