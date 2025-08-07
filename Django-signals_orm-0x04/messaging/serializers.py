# messaging/serializers.py

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'receiver',
            'content',
            'timestamp',
            'read',
        ]


    def get_sender(self, obj):
        return {"id": obj.sender.id, "username": obj.sender.username}

    def get_receiver(self, obj):
        return {"id": obj.receiver.id, "username": obj.receiver.username}