from django.http import Http404
from django.db.models import Q
from django.views.generic import ListView, View, DetailView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as User_mixins
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition"""

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "-created"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                # print(request.GET)
                # url에 있는 data
                # print(form)
                # url에 있는 data를 이용하여 form html을 만듬
                # print(form.cleaned_data)
                # forms.py를 참고해서 form html에 담겨있는 필요한 정보만 가져옴 & 정제(ex, str > int)
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                """ filter """
                filter_args = Q()

                if city != "Anywhere":
                    filter_args &= Q(city__startswith=city)

                filter_args &= Q(country=country)

                if room_type is not None:
                    filter_args &= Q(room_type=room_type)

                if price is not None:
                    filter_args &= Q(price__lte=price)

                if guests is not None:
                    filter_args &= Q(guests__gte=guests)

                if bedrooms is not None:
                    filter_args &= Q(bedrooms__gte=bedrooms)

                if beds is not None:
                    filter_args &= Q(beds__gte=beds)

                if baths is not None:
                    filter_args &= Q(baths__gte=baths)

                if instant_book is True:
                    filter_args &= Q(instant_book=True)

                if superhost is True:
                    filter_args &= Q(host__superhost=True)

                qs = models.Room.objects.filter(filter_args)

                for amenity in amenities:
                    # rooms = rooms & models.Room.objects.filter(amenities=amenity)
                    qs = qs.filter(amenities=amenity)

                for facility in facilities:
                    # rooms = rooms & models.Room.objects.filter(facilities=facility)
                    qs = qs.filter(facilities=facility)

                qs = qs.order_by("-created")

                paginator = Paginator(qs, 10)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                """ query_string 만들기_Pagination """

                urlencode = request.GET.urlencode()

                query_list = [i for i in urlencode.split("&") if "page=" not in i]

                """
                복잡한 버전
                query_list = []
                for i in urlencode.split("&"):
                    if "page=" not in i:
                        query_list.append(i)
                """

                query_string = "&".join(query_list)

                return render(
                    request,
                    "rooms/room_search.html",
                    {"form": form, "rooms": rooms, "query_string": query_string},
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/room_search.html", {"form": form})


class EditRoomView(User_mixins.LoggedInOnlyView, UpdateView):
    """ 숙소를 수정하기 위한 View """

    model = models.Room
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rule",
    )
    template_name = "rooms/room_edit.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(User_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "⛔ 사진을 삭제할 수 없습니다.")
            return redirect(reverse("core:home"))
        else:
            # photo_pk가 올바르지 않은 경우: 새로고침
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "✔ 사진을 삭제했습니다.")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        messages.error(request, "존재하지 않는 숙소입니다.")
        return redirect(reverse("core:home"))


class EditPhotoView(User_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    """ 숙소 사진 수정 View """

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "✔ 사진을 수정했습니다."

    # Model.Photo에서 get_absolute_url을 통해 같은 방식을 취할 수 있음
    # def get_success_url(self):
    #     room_pk = self.kwargs.get("room_pk")
    #     return reverse("room:photos", kwargs={'pk': room_pk})
