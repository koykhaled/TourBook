from django.db import models

from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager
# Create your models here.

class Role(models.TextChoices):
    ADVERTISER = "AD", "Advertiser"
    CLIENT = "C", "Client"
    ORGANIZER = "O", "Organizer"


    def getRoleKeys():
        keys = [key for key, _ in Role.choices]
        return keys

class UserAccountManager(BaseUserManager):
    def create_user(self,name,phone,email,password=None):
        
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
        if not email :
            raise ValueError("User must Have an Email Address")
        
        email = self.normalize_email(email)
        
        user = self.model(name=name ,phone=phone,email=email)
        
        user.set_password(password)
        
        user.save()
        
        return user
    
    
    def create_superuser(self,name , phone,email,password=None):
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
        user = self.create_user(name=name,phone=phone,email=email,password=password)
        
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class UserAccount(AbstractBaseUser,PermissionsMixin):
    """
    Custom user model representing a user account.
    """
    
    name = models.CharField(max_length=255)
    
    phone = models.CharField(max_length=20,unique=True)
    
    email = models.EmailField(max_length=100,unique=True)
    
    is_active = models.BooleanField(default=True)
    
    is_staff = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True)
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['name','phone']
    
    def getUserName(self):
        return self.user_name
    
    def __str__(self):
        return self.email

