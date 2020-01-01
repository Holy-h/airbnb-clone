from django.db import models


class TimeStampedModel(models.Model):

    """ Time Stamped Model """

    # Toknow - "auto_now_add: DB에 올라갈 때, auto_now: 업데이트 되었을 때"
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Toknow - "나는 이 모델이 데이터베이스에 적용되는 걸 원치 않아"
    class Meta:
        abstract = True
