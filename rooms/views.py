from math import ceil
from django.shortcuts import render
from . import models


def all_rooms(request):
    request_page = request.GET.get("page", 1)
    page = int(request_page or 1)
    # request_page가 null인 경우

    if page < 1:
        page = 1
    # request_page가 1보다 작은 경우

    page_size = 10
    limit = page * page_size
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = ceil(models.Room.objects.count() / page_size)
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "page": page,
            "page_count": page_count,
            "page_range": range(1, page_count+1),
        },
    )
