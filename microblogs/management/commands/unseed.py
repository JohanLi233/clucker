from django.core.management.base import BaseCommand, CommandError
from microblogs.models import User;


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            if user.username != "@Jaha":
                user.delete()
                print(user)
