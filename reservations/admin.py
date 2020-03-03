from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    """ BookedDay Admin Definition """

    list_display = ("day", "get_room_name", "get_room_guest")

    def get_room_name(self, obj):
        return obj.reservation.room.name

    get_room_name.short_description = "room name"

    def get_room_guest(self, obj):
        return obj.reservation.guest

    get_room_guest.short_description = "room guest"
