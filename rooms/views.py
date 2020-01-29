from django.shortcuts import render
from . import models


def all_rooms(request):
    page = int(request.GET.get("page", 1))
    if page < 1:
        page = 1
    page_size = 10
    offset = page * page_size - page_size
    limit = page * page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    return render(request, "rooms/home.html", context={"rooms": all_rooms})
