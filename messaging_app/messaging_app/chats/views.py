from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.db.models import Q

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']  # Allow filtering by creation date

    def get_queryset(self):
        """
        Return conversations where the requesting user is a participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def perform_create(self, serializer):
        """
        Create a new conversation and add the requesting user as a participant.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages in a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sent_at', 'sender']  # Allow filtering by sent_at and sender

    def get_queryset(self):
        """
        Return messages for a specific conversation where the user is a participant.
        """
        user = self.request.user
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(
                conversation__conversation_id=conversation_id,
                conversation__participants=user
            )
        return Message.objects.filter(conversation__participants=user)

    def perform_create(self, serializer):
        """
        Create a new message, setting the sender to the requesting user.
        """
        conversation_id = self.kwargs.get('conversation_id')
        conversation = Conversation.objects.get(conversation_id=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)