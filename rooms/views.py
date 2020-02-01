from django.shortcuts import render
from django.core.paginator import Paginator
from . import models


def all_rooms(request):
    request_page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(request_page)
    print(vars(rooms.paginator))
    return render(request, "rooms/home.html", {"rooms": rooms})

