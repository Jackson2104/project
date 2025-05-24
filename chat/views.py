from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_users(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat_users.html', {'users': users})

@login_required
def chat_view(request, user_id):
    other_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            Message.objects.create(sender=request.user, receiver=other_user, message=msg)
            return redirect('chat_view', user_id=other_user.id)

    return render(request, 'chat/chat_room.html', {
        'messages': messages,
        'other_user': other_user
    })

