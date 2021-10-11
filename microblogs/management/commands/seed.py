from django.core.management.base import BaseCommand, CommandError
from faker import Faker

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('zh_CN')
        
    def handle(self, *args, **options):
        print("1234")
