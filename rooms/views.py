from django.views.generic import ListView
from django.http import Http404
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """ HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        # 404 NotFund
        raise Http404()


def search(request):
    search_keyword = request.GET.get("city", "Anywhere")
    search_keyword = str.capitalize(search_keyword)
    room_types = models.RoomType.objects.all()
    return render(
        request,
        "rooms/room_search.html",
        context={"city": search_keyword, "countries": countries, "room_types": room_types},
    )
