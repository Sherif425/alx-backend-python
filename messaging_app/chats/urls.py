from django.urls import path, include  # ✅ path, include
from rest_framework.routers import DefaultRouter  # ✅ DefaultRouter()

from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),  # ✅ path and include used
]
