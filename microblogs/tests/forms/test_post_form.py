from django.test import TestCase
from microblogs.models import User, Post
from microblogs.forms import PostForm

class PostFormTestCase(TestCase):
    fixtures=['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(username='@johndoe')

    def test_valid_post_form(self):
        input = {'text': 'x'*200 }
        form = PostForm(data=input)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        input = {'text': 'x'*600 }
        form = PostForm(data=input)
        self.assertFalse(form.is_valid())
