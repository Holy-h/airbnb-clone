from django.db.models import Q
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
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    # from request
    form = {
        "s_city": city,
        "s_country": country,
        "s_room_type": room_type,
        "s_price": price,
        "s_guests": guests,
        "s_bedrooms": bedrooms,
        "s_beds": beds,
        "s_baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    # from DB
    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # filter
    filter_args = Q()

    if city != "Anywhere":
        filter_args &= Q(city__startswith=city)

    filter_args &= Q(country=country)

    if room_type != 0:
        filter_args &= Q(room_type=room_type)

    if price != 0:
        filter_args &= Q(price__lte=price)

    if guests != 0:
        filter_args &= Q(guests__gte=guests)

    if bedrooms != 0:
        filter_args &= Q(bedrooms__gte=bedrooms)

    if beds != 0:
        filter_args &= Q(beds__gte=beds)

    if baths != 0:
        filter_args &= Q(baths__gte=baths)

    if instant is True:
        filter_args &= Q(instant_book=True)

    if superhost is True:
        filter_args &= Q(host__superhost=True)

    rooms = models.Room.objects.filter(filter_args)

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            rooms = rooms & models.Room.objects.filter(amenities__pk=int(s_amenity))

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            rooms = rooms & models.Room.objects.filter(facilities__pk=int(s_facility))

    # print(filter_args)

    print(rooms)

    return render(
        request, "rooms/room_search.html", context={**form, **choices, "rooms": rooms}
    )