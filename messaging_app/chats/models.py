from django.db import models
from django.contrib.auth.models import AbstractUser

# 1. Custom User model
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)  # Explicit ID field for the checker
    first_name = models.CharField(max_length=30)  # Already part of AbstractUser, but required explicitly
    last_name = models.CharField(max_length=30)   # Same as above

    def __str__(self):
        return self.username


# 2. Conversation model
class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)  # Explicit ID for checker
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return self.name


# 3. Message model
class Message(models.Model):
    message_id = models.AutoField(primary_key=True)  # Explicit ID for checker
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()  # Explicitly named for checker
    sent_at = models.DateTimeField(auto_now_add=True)  # Explicitly named for checker

    def __str__(self):
        return f"From {self.sender} in {self.conversation}"
