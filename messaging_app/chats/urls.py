from django.urls import path
from .auth import AuthCheckView

urlpatterns = [
    path('auth-check/', AuthCheckView.as_view(), name='auth_check'),
]