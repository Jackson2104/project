# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.http import HttpResponseForbidden
from .models import Message

@login_required
def delete_message(request, message_id):
    msg = Message.objects.get(id=message_id)

    if request.user.role != 'kiongozi':
        return HttpResponseForbidden("Huna ruhusa ya kufuta ujumbe huu.")

    msg.delete()
    django_messages.success(request, "Ujumbe umefutwa.")
    return redirect('chat_room')

@login_required
def chat_room(request):
    chat_messages = Message.objects.all().order_by('timestamp')

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            Message.objects.create(sender=request.user, message=msg)
            return redirect('chat_room')

    # 👇 Chagua template sahihi kulingana na role
    if request.user.role == 'kiongozi':
        template_name = 'kiongozi/chat_room.html'
    else:
        template_name = 'mwananchi/chat_room.html'

    return render(request, template_name, {
        'chat_messages': chat_messages
    })

