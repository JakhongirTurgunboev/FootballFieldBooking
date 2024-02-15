from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username or not password:
            raise ValueError('The phone number must be set')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # Ensure that only superusers can be created using this method
        extra_fields.setdefault('user_role', 'A')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    USER_ROLES = (
        ('A', 'Administrator'),
        ('O', 'Pitch Owner'),
        ('U', 'User')
    )

    phone_number = models.CharField(max_length=13)
    user_role = models.CharField(max_length=1, choices=USER_ROLES, default='U')
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
