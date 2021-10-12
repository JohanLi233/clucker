"""Unit Test for the sign up form"""
from django import forms
from django.test import TestCase
from microblogs.forms import SignUpForm
from microblogs.models import User
from django.core.exceptions import ValidationError

class SignUpViewTestCase(TestCase):
    """Tests of the sign up view."""
    #Form accept valid input data
    def setUp(self):
         self.form_input = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'username': '@janedoe',
        'email': 'janedoe@example.org',
        'bio': 'My bio',
        'new_password': 'Password123',
        'confirm_password': 'Password123'
         }

    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('confirm_password', form.fields)
        password_confirmation_widget = form.fields['confirm_password'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['confirm_password'] = 'password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['confirm_password'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['confirm_password'] = 'PasswordABC'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['confirm_password'] = 'WrongPassword123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    #
    # def test_sign_up_url(self):
    #     self.assertEqual(self.url,'/sign_up/')
    #
    # def test_get_sign_up(self):
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'sign_up.html')
    #     form = response.context['form']
    #     self.assertTrue(isinstance(form, SignUpForm))
    #     self.assertFalse(form.is_bound)
    #
    # def test_unsuccesful_sign_up(self):
    #     self.form_input['username'] = 'BAD_USERNAME'
    #     before_count = User.objects.count()
    #     response = self.client.post(self.url, self.form_input)
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count, before_count)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'sign_up.html')
    #     form = response.context['form']
    #     self.assertTrue(isinstance(form, SignUpForm))
    #     self.assertTrue(form.is_bound)
    #
    # def test_succesful_sign_up(self):
    #     before_count = User.objects.count()
    #     response = self.client.post(self.url, self.form_input, follow=True)
    #     after_count = User.objects.count()
    #     self.assertEqual(after_count, before_count+1)
    #     response_url = reverse('feed')
    #     self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'feed.html')
    #     user = User.objects.get(username='@janedoe')
    #     self.assertEqual(user.first_name, 'Jane')
    #     self.assertEqual(user.last_name, 'Doe')
    #     self.assertEqual(user.email, 'janedoe@example.org')
    #     self.assertEqual(user.bio, 'My bio')
    #     is_password_correct = check_password('Password123', user.password)
    #     self.assertTrue(is_password_correct)
