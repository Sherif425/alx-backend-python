from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Message
from django.db.models import Prefetch


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # Or any post-delete page






@login_required
def conversation_view(request):
    # Get root messages (no parent)
    root_messages = Message.objects.filter(
        receiver=request.user, parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
    ).order_by('-timestamp')

    context = {'messages': root_messages}
    return render(request, 'messaging/conversation.html', context)


# messaging/views.py

from django.db.models import Prefetch
from .models import Message

def get_user_conversations(user):
    """
    Returns all root messages and their replies for a user efficiently.
    """
    root_messages = (
        Message.objects
        .filter(receiver=user, parent_message__isnull=True)
        .select_related('sender', 'receiver')  # optimize FK access
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        .order_by('-timestamp')
    )
    return root_messages


# messaging/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    serializer = MessageSerializer(unread_messages, many=True)
    return Response(serializer.data)


