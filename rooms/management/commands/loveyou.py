from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "This command tells me that she loves me"

    def add_arguments(self, parser):
        parser.add_argument("--times", help="How many times")

    def handle(self, *args, **options):
        times = options.get("times")
        for i in range(0, int(times)):
            self.stdout.write(self.style.SUCCESS(f"I love you {i}times"))
