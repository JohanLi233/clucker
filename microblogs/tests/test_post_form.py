from django import forms
from django.test import TestCase
from microblogs.forms import PostForm

class PostFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
        'text': 'I am the text'
        }

    def test_valid_post_form(self):
        form = PostForm(data=self.form_input)
        self.assertTrue(form.is_valid())
