from django.shortcuts import redirect, reverse
from django.contrib import messages
from rooms import models as room_models
from . import forms


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            messages.error(request, "리뷰를 남길 숙소를 찾을 수 없어요 ㅠㅠ")
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            # form.save 메소드를 변경하여, form 정보를 return받은 후

            review.room = room
            review.user = request.user
            review.save()
            # form 데이터 중 직접 입력받지 않은 일부 정보를 추가한 후에 db에 직접 저장한다

            messages.success(request, "리뷰가 작성되었습니다.")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

        messages.warning(request, "리뷰를 남길 수 없어요.")
        return redirect(reverse("core:home"))
        # Todo
