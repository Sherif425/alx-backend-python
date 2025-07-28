from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Initialize the DefaultRouter
router = DefaultRouter()
# Register ConversationViewSet for /api/conversations/
router.register(r'conversations', ConversationViewSet, basename='conversation')
# Register MessageViewSet for /api/conversations/<conversation_id>/messages/
router.register(r'conversations/(?P<conversation_id>[^/.]+)/messages', MessageViewSet, basename='message')

# Include router URLs in urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),
]