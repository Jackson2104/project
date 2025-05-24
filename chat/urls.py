from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.chat_users, name='chat_users'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),
]
