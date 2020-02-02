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
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 1))
    room_types = models.RoomType.objects.all()

    # from request
    form = {
        "s_city": city,
        "s_country": country,
        "s_room_type": room_type,
    }

    # from DB
    choices = {
        "countries": countries,
        "room_types": room_types,
    }

    return render(request, "rooms/room_search.html", context={**form, **choices},)
