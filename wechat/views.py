from django.shortcuts import render , redirect
from .models import ChatRoom
from .forms import ChatRoomForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required 

@login_required
def index(request):
    print(ChatRoom.objects.all())
    ctx = {
        'form': ChatRoomForm(), 
        'rooms': ChatRoom.objects.all()
    }
    return render(request, "chat/index.html" ,ctx)


@login_required
def room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    return render(request, 'chat/room.html', {'room_name': room_name})

@login_required
def create_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            chat_room = form.save()
            return redirect(reverse_lazy('room', kwargs={'room_name': chat_room.name}))
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login'))