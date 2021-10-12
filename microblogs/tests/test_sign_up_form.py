"""Unit Test for the sign up form"""
from django.test import TestCase
from microblogs.forms import SignUpForm
from microblogs.models import User
from django.core.exceptions import ValidationError

class SignUpFormTestCase(TestCase):
    """Unit Test for the sign up form"""
