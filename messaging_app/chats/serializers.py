from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, exposing relevant fields.
    """
    # Using CharField for email to ensure it's treated as a string with validation
    email = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']

    def validate_email(self, value):
        """
        Custom validation for email to ensure uniqueness.
        """
        if User.objects.filter(email=value).exclude(user_id=self.instance.user_id if self.instance else None).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model, including sender details.
    """
    sender = UserSerializer(read_only=True)
    # Using CharField for message_body to enforce specific validation
    message_body = serializers.CharField(min_length=1, max_length=5000)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']

    def validate(self, attrs):
        """
        Ensure the conversation exists and the sender is a participant.
        """
        conversation = attrs.get('conversation')
        sender = self.context['request'].user  # Assuming sender is set via request context
        if conversation and sender not in conversation.participants.all():
            raise serializers.ValidationError("Sender must be a participant in the conversation.")
        return attrs

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model, including nested participants and messages.
    """
    # Using SerializerMethodField for custom participants representation
    participants = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True, source='messages.all')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_participants(self, obj):
        """
        Custom method to serialize participants as a list of email addresses.
        """
        return [user.email for user in obj.participants.all()]

    def validate(self, attrs):
        """
        Ensure at least two participants are provided when creating/updating a conversation.
        """
        if self.context.get('request').method in ['POST', 'PUT', 'PATCH']:
            participants = self.initial_data.get('participants', [])
            if len(participants) < 2:
                raise serializers.ValidationError("A conversation must have at least two participants.")
        return attrs