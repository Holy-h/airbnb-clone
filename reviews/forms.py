from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    """ Review Form """

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def save(self, commit=False):
        review = super().save(commit=commit)
        return review
