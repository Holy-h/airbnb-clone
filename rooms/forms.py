from django import forms
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere", required=False)
    price = forms.IntegerField(required=False)
    room_type = forms.ModelChoiceField(queryset=models.RoomType.objects.all())
