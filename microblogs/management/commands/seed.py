from django.core.management.base import BaseCommand, CommandError

from microblogs.models import User
from microblogs.models import Post

import pytz
from faker import Faker
from random import randint, random


class Command(BaseCommand):
    USER_COUNT = 100
    POST_COUNT = 2000
    FOLLOW_PROBABILITY = 0.1
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.create_posts()
        self.create_followers()

    def create_users(self):
        self.create_johndoe()
        user_count = 1
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            try:
                self.create_user()
            except:
                continue
            user_count += 1
        print("User seeding complete.      ")

    def create_johndoe(self):
        User.objects.create_user(
            username='@janedoe',
            email='janedoe@example.org',
            password=self.DEFAULT_PASSWORD,
            first_name='Jane',
            last_name='Doe',
            bio="Hi, I'm Jane Doe and want to remain anonymous here.  "
                "This is a sample account for development purposes."
        )

    def create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        bio = self.faker.text(max_nb_chars=520)
        User.objects.create_user(
            username=username,
            email=email,
            password=Command.DEFAULT_PASSWORD,
            first_name=first_name,
            last_name=last_name,
            bio=bio
        )

    def create_posts(self):
        for i in range(self.POST_COUNT):
            print(f"Seeding post {i}/{self.POST_COUNT}", end='\r')
            self.create_post()
        print("Post seeding complete.      ")

    def create_post(self):
        post = Post()
        post.author = self.get_random_user()
        post.text = self.faker.text(max_nb_chars=280)
        post.save()
        datetime = self.faker.past_datetime(start_date='-365d', tzinfo=pytz.UTC)
        Post.objects.filter(id=post.id).update(created_at = datetime)

    def get_random_user(self):
        index = randint(0,self.users.count()-1)
        return self.users[index]

    def create_followers(self):
        count = 1
        for user in self.users:
            print(f"Seed followers for user {count}/{self.USER_COUNT}", end='\r')
            self.create_followers_for_user(user)
            count += 1
        print("Follower seeding complete.     ")

    def create_followers_for_user(self, user):
        for follower in self.users:
            if random() < self.FOLLOW_PROBABILITY:
                user.toggle_follow(follower)

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'
