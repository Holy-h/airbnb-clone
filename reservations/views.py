import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import redirect, reverse, render
from rooms import models as room_models
from . import models as reservation_models


class CreateError(Exception):
    """ Exception Error class """

    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        reservation_models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError("이미 예약되어 있어요")

    except room_models.Room.DoesNotExist:
        messages.error(request, "이 숙소는 예약할 수 없습니다😰")
        return redirect(reverse("core:home"))

    except CreateError as error_context:
        messages.error(request, error_context)
        return redirect(reverse("core:home"))

    except reservation_models.BookedDay.DoesNotExist:
        reservation = reservation_models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    """ View of Reservation Detail """

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
        is_guest = reservation.guest == self.request.user
        is_host = reservation.room.host == self.request.user

        if not reservation or (not is_host and not is_guest):
            raise Http404()
        return render(
            self.request, "reservations/detail.html", {"reservation": reservation}
        )


def edit_reservation(request, pk, verb):
    reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
    is_guest = reservation.guest == request.user
    is_host = reservation.room.host == request.user

    if not reservation or (not is_host and not is_guest):
        raise Http404()

    print(reservation.status)
    print(reservation.room.name)

    if verb == "confirm":
        reservation.status = reservation_models.Reservation.STATUS_CONFIRMED
        print("확인 됨")
    elif verb == "cancel":
        print("취소 됨")
        reservation.status = reservation_models.Reservation.STATUS_CANCELED

    print(reservation.status)
    reservation.save()
    messages.success(request, "예약 내용이 변경되었습니다")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
