"""Tests of the feed view."""
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from microblogs.forms import PostForm
from microblogs.models import User
from microblogs.tests.helpers import create_posts, reverse_with_next


class FeedViewTestCase(TestCase):
    """Tests of the feed view."""

    fixtures = [
        'microblogs/tests/fixtures/default_user.json',
        'microblogs/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('feed')

    def test_feed_url(self):
        self.assertEqual(self.url,'/feed/')

    def test_get_feed(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)

    def test_get_feed_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_feed_contains_posts_by_self_and_followees(self):
        self.client.login(username=self.user.username, password='Password123')
        jane = User.objects.get(username='@janedoe')
        petra = User.objects.get(username='@petrapickles')
        peter = User.objects.get(username='@peterpickles')
        create_posts(self.user, 100, 103)
        create_posts(jane, 200, 203)
        create_posts(petra, 300, 303)
        create_posts(peter, 400, 403)
        self.user.toggle_follow(jane)
        self.user.toggle_follow(petra)
        response = self.client.get(self.url)
        for count in range(100, 103):
            self.assertContains(response, f'Post__{count}')
        for count in range(200, 203):
            self.assertContains(response, f'Post__{count}')
        for count in range(300, 303):
            self.assertContains(response, f'Post__{count}')
        for count in range(400, 403):
            self.assertNotContains(response, f'Post__{count}')
        self.assertFalse(response.context['is_paginated'])

    def test_feed_with_pagination(self):
        self.client.login(username=self.user.username, password='Password123')
        jane = User.objects.get(username='@janedoe')
        self.user.toggle_follow(jane)
        create_posts(self.user, 100, 100+settings.POSTS_PER_PAGE+2)
        create_posts(jane, 100, 100+settings.POSTS_PER_PAGE+2)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        self.assertTrue(response.context['is_paginated'])
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_one_url = self.url + '?page=1'
        response = self.client.get(page_one_url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertFalse(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_two_url = self.url + '?page=2'
        response = self.client.get(page_two_url)
        self.assertEqual(len(response.context['posts']), settings.POSTS_PER_PAGE)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertTrue(page_obj.has_next())
        page_three_url = self.url + '?page=3'
        response = self.client.get(page_three_url)
        self.assertEqual(len(response.context['posts']), 4)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())
