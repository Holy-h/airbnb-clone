from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from django.contrib import messages
from rooms import models as room_models
from . import models as list_models


def toggle_room(request, room_pk):
    action = request.GET.get("action", None)

    previous_url = request.META.get("HTTP_REFERER")

    user = request.user

    if not user.is_authenticated:
        messages.error(request, "로그인이 필요합니다.")
        return redirect(reverse("users:login"))

    room = room_models.Room.objects.get_or_none(pk=room_pk)

    if room is not None and action is not None:
        the_list, _ = list_models.List.objects.get_or_create(
            user=request.user, name="My Favorite Houses"
        )

        if action == "add":
            the_list.rooms.add(room)
            messages.success(request, "이 숙소를 관심 숙소에 저장했어요.")

        if action == "remove":
            the_list.rooms.remove(room)
            messages.success(request, "이 숙소를 관심 숙소에서 삭제했어요.")

    else:
        messages.error(request, "올바르지 않은 접근입니다.")

    if "rooms" in previous_url:
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
    elif "lists" in previous_url:
        return redirect(reverse("lists:see-favs"))
    else:
        return redirect(reverse("core:home"))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"
