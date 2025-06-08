from django.urls import path
from . import views

urlpatterns = [ 
    path('chat/', views.chat_room, name='chat_room'),
    path('chat/delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
