from django.test import TestCase
from microblogs.models import User
from microblogs.views import UserListView

class UserListTestCase(TestCase):
    def test_same_user_count(self):
        before = User.objects.count()
        #UserListView.get_context_data()
        self.assertEqual(before, User.objects.count())
