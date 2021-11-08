from django.test import TestCase
from django.urls import reverse
from microblogs.models import User

class UserListTest(TestCase):
    def setUp(self):
        self.url = reverse('user_list')

    def test_user_list_url(self):
        self.assertEqual(self.url,'/users/')

    def test_get_user_list(self):
        self._create_test_users(15)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        self.assertEqual(len(response.context['users']), 15)
        for user_id in range(15):
            self.assertContains(response, f'@user{user_id}')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            user = User.objects.get(username=f'@user{user_id}')
            user_url = reverse('show_user', kwargs={'user_id': user.id})
            self.assertContains(response, user_url)

    def _create_test_users(self, user_count=10):
        for user_id in range(user_count):
            User.objects.create_user(f'@user{user_id}',
                email=f'user{user_id}@test.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio {user_id}',
            )
