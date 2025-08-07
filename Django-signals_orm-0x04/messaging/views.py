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
