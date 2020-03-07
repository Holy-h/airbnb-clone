from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    """ Seed House Rules """

    help = "This command creates houseRules"

    def handle(self, *args, **options):
        houseRules = [
            "어린이(2~12세) 숙박에 적합함",
            "유아(2세 미만) 숙박에 적합함",
            "반려동물 동반에 적합함",
            "흡연 가능",
            "행사나 파티 허용",
        ]

        for item in houseRules:
            room_models.HouseRule.objects.create(name=item)

        self.stdout.write(
            self.style.SUCCESS(f"SUCCESS: {len(houseRules)} houseRules created")
        )
