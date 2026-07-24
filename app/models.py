from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=False)
    age = models.PositiveIntegerField( blank=False)
    bio = models.TextField(blank=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number','age']

    objects = CustomUserManager()

    def __str__(self):
        return self.email