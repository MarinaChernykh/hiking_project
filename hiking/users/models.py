from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Customized User model to make email field required."""
    email = models.EmailField('Email', blank=False, unique=True)
