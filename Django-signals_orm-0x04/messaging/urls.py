from django.urls import path
from . import views
from .views import message_list_view 

urlpatterns = [
    path('delete_account/', views.delete_user, name='delete_user'),
    path('messages/', MessageListView.as_view(), name='message_list'),
]
