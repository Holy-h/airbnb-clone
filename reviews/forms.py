from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    """ Review Form """

    accuracy = forms.IntegerField(min_value=1, max_value=5)
    communication = forms.IntegerField(min_value=1, max_value=5)
    cleanliness = forms.IntegerField(min_value=1, max_value=5)
    location = forms.IntegerField(min_value=1, max_value=5)
    check_in = forms.IntegerField(min_value=1, max_value=5)
    value = forms.IntegerField(min_value=1, max_value=5)

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
