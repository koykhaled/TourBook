from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.contrib.auth.hashers import make_password
import re
# Create your models here.


class Role(models.TextChoices):
    ADVERTISER = "AD", "Advertiser"
    CLIENT = "C", "Client"
    ORGANIZER = "O", "Organizer"

    def getRoleKeys():
        keys = [key for key, _ in Role.choices]
        return keys


class UserAccountManager(BaseUserManager):
    def create_user(self, username, phone, email, role, password=None):
        """
        Creates a user with the provided details.

        Args:
            name (str): The name of the user.
            phone (str): The phone number of the user.
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            user (object): The created user object.
        """
        if not email:
            raise ValueError("User must Have an Email Address")

        email = self.normalize_email(email)

        user = self.model(username=username, phone=phone,
                          email=email, role=role)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, phone, email, role, password=None):
        """
        Create and save a superuser with the given name, phone, email, and password.

        Args:
            name (str): The name of the superuser.
            phone (str): The phone number of the superuser.
            email (str): The email address of the superuser.
            password (str, optional): The password for the superuser. Defaults to None.

        Returns:
            User: The created superuser instance.
    """
        user = self.create_user(username=username, phone=phone,
                                email=email, password=password, role=role)

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user account.
    All User Types Model (Advertiser , Client , Organizer) Should be null for Manual Inserting 
    only user_id should be fill automatic => sync with user regisetration
    """

    username = models.CharField(max_length=255, unique=True)

    phone = models.CharField(max_length=20, unique=True)

    email = models.EmailField(max_length=100, unique=True)

    is_active = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)

    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.CLIENT)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['phone', 'role']

    def getUserName(self):
        return self.username

    def __str__(self):
        return self.email
