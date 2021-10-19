from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from microblogs.models import User;

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        for i in range(100):
            user = User(
                username = '@' + self.faker.user_name(),
                first_name = self.faker.first_name(),
                last_name = self.faker.last_name(),
                bio = 'I am a fake user',
                email = self.faker.ascii_email()
                )
            user.save()
            print(user)
