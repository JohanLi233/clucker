from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    username = models.CharField(
    max_length = 30,
    unique = True,
    validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must constis of @ followed at least three alphanumericals'
        )]
    )
    first_name = models.CharField(
    blank = False,
    unique = False,
    max_length = 50
    )
    last_name = models.CharField(
    blank = False,
    unique = False,
    max_length = 50
    )
    bio = models.CharField(
    blank = True,
    unique = False,
    max_length = 520
    )
    email = models.EmailField(
    unique = True,
    blank = False
    )

class Post(models.Model):
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        blank = False
    )
    text = models.CharField(
        max_length = 280
    )
    created_at = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
