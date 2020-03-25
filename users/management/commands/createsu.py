from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **kwargs):

        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:

            User.objects.create_superuser("ebadmin", "kepy1106@gmail.com", "123123")
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))

        else:

            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
