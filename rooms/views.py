from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models


def all_rooms(request):
    request_page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        room_page = paginator.page(int(request_page))
        return render(request, "rooms/home.html", {"Page": room_page})
    except EmptyPage:
        room_page = paginator.page(1)
        return redirect("/")

