from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from microblogs.models import User, Post
from microblogs.tests.helpers import create_posts, reverse_with_next
from with_asserts.mixin import AssertHTMLMixin

class ShowUserTest(TestCase, AssertHTMLMixin):

    fixtures = [
        'microblogs/tests/fixtures/default_user.json',
        'microblogs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.target_user = User.objects.get(username='@janedoe')
        self.url = reverse('show_user', kwargs={'user_id': self.target_user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/user/{self.target_user.id}')

    def test_get_show_user_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "@janedoe")
        followable = response.context['followable']
        self.assertTrue(followable)
        follow_toggle_url = reverse('follow_toggle', kwargs={'user_id': self.target_user.id})
        query = f'.//form[@action="{follow_toggle_url}"]//button'
        with self.assertHTML(response) as html:
            button = html.find(query)
            self.assertEquals(button.text, "Follow")
        self.user.toggle_follow(self.target_user)
        response = self.client.get(self.url)
        with self.assertHTML(response) as html:
            button = html.find(query)
            self.assertEquals(button.text, "Unfollow")

    def test_get_show_user_with_own_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, "John Doe")
        self.assertContains(response, "@johndoe")
        followable = response.context['followable']
        self.assertFalse(followable)
        follow_toggle_url = reverse('follow_toggle', kwargs={'user_id': self.target_user.id})
        query = f'.//form[@action="{follow_toggle_url}"]//button'
        with self.assertHTML(response) as html:
            button = html.find(query)
            self.assertIsNone(button)

    def test_get_show_user_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')

    def test_get_show_user_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_show_user_displays_posts_belonging_to_the_shown_user_only(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='@janedoe')
        create_posts(other_user, 100, 103)
        create_posts(self.user, 200, 203)
        url = reverse('show_user', kwargs={'user_id': other_user.id})
        response = self.client.get(url)
        for count in range(100, 103):
            self.assertContains(response, f'Post__{count}')
        for count in range(200, 203):
            self.assertNotContains(response, f'Post__{count}')
        self.assertFalse(response.context['is_paginated'])

    def test_show_user_displays_posts_with_pagination(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='@janedoe')
        create_posts(other_user, 100, 100+(settings.POSTS_PER_PAGE * 2)+3)
        url = reverse('show_user', kwargs={'user_id': other_user.id})
        response = self.client.get(url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        self.assertTrue(response.context['is_paginated'])
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_one_url = url + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        self.assertFalse(page_obj.has_previous())
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_next())
        page_two_url = url + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_three_url = url + '?page=3'
        response = self.client.get(page_three_url)
        self.assertEqual(len(response.context['posts']), 3)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())
