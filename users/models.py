from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "male"),
        (GENDER_FEMALE, "female"),
        (GENDER_OTHER, "other"),
    )

    avatar = models.ImageField(null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=GENDER_MALE,
        max_length=10,
        null=True,
        blank=True,
    )
    bio = models.TextField(default="", blank=True)
