from django.core.management.base import BaseCommand
from rooms import models as room_models


class Command(BaseCommand):
    help = "This command creates facilities"

    # def add_arguments(self, parser):
    #     parser.add_argument("--times", help="How many times")

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid Parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]

        for item in facilities:
            room_models.Facility.objects.create(name=item)
        self.stdout.write(
            self.style.SUCCESS(f"SUCCESS: {len(facilities)} Facilities created!")
        )
