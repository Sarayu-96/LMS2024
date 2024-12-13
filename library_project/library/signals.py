from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, Notification,User

@receiver(post_save, sender=Book)
def notify_new_book(sender, instance, created, **kwargs):
    if created:  # Only notify on new book creation
        users = User.objects.all()  # Notify all users
        message = f"New Book Alert: '{instance.title}' by {instance.author.name} is now available in our library!"
        for user in users:
            Notification.objects.create(user=user, message=message)

            