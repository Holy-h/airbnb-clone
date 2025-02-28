from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField(
        validators=[
            MaxValueValidator(5, message="1~5 사이의 수를 입력하세요"),
            MinValueValidator(1, message="1~5 사이의 수를 입력하세요"),
        ]
    )
    communication = models.IntegerField(
        validators=[
            MaxValueValidator(5, message="1~5 사이의 수를 입력하세요"),
            MinValueValidator(1, message="1~5 사이의 수를 입력하세요"),
        ]
    )
    cleanliness = models.IntegerField(
        validators=[
            MaxValueValidator(5, message="1~5 사이의 수를 입력하세요"),
            MinValueValidator(1, message="1~5 사이의 수를 입력하세요"),
        ]
    )
    location = models.IntegerField(
        validators=[
            MaxValueValidator(5, message="1~5 사이의 수를 입력하세요"),
            MinValueValidator(1, message="1~5 사이의 수를 입력하세요"),
        ]
    )
    check_in = models.IntegerField(
        validators=[
            MaxValueValidator(5, message="1~5 사이의 수를 입력하세요"),
            MinValueValidator(1, message="1~5 사이의 수를 입력하세요"),
        ]
    )
    value = models.IntegerField(
        validators=[
            MaxValueValidator(5, message="1~5 사이의 수를 입력하세요"),
            MinValueValidator(1, message="1~5 사이의 수를 입력하세요"),
        ]
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room.name}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."

    class Meta:
        ordering = ("-created",)

