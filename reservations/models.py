import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models
from . import managers


class BookedDay(core_models.TimeStampedModel):
    """ BookedDay Model Definition """

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return f"{self.day}_{self.reservation.room.name}"


class Reservation(core_models.TimeStampedModel):

    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRM = "confirm"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRM, "Confirm"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    objects = managers.CustomReservationManager()

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        # if self.pk is None:
        if True:
            check_in = self.check_in
            check_out = self.check_out
            period = check_out - check_in
            is_booked = BookedDay.objects.filter(
                day__range=(check_in, check_out), reservation__room=self.room
            ).exists()
            if not is_booked:
                super().save(*args, **kwargs)
                # ↓ 시작을 포함하는 경우에는 1을 더해준다
                for i in range(period.days + 1):
                    day = check_in + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        else:
            return super().save(*args, **kwargs)
