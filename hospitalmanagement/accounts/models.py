from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class CustomUser(AbstractUser):
    role_choices = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ]

    username = None     # By passing username
    phone = models.CharField(max_length=10, unique=True)
    role = models.CharField(choices=role_choices, default='patient', max_length=7)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email', 'role']

    objects = UserManager()

    def __str__(self):
        return self.first_name