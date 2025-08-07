from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if the message is new (not an update)

    try:
        original = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if original.content != instance.content:
        # Save history
        MessageHistory.objects.create(
            message=original,
            old_content=original.content
        )
        instance.edited = True  
        


User = get_user_model()

@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    # Automatically deletes related objects due to CASCADE, but if needed explicitly:
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
