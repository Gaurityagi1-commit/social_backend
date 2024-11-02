from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .manager import UserProfileManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, username, password, **extra_fields)
    

    def get_all_users(self):
        return self.all()
    
    def get_all_active_users(self):
        return self.filter(is_active=True)
    
    def search_user(self,query):
        user = self.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        return user
    




class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), unique=True, max_length=20)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    # Additional fields specific to e-commerce
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True, null=True)
    address = models.TextField(_('address'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    state = models.CharField(_('state'), max_length=100, blank=True, null=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True, null=True)
    country = models.CharField(_('country'), max_length=100, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email','first_name','last_name']

    def __str__(self):
        return self.username




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default='default_profile.png')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()

    def __str__(self):
        return f'{self.user.username} + {self.bio}'
    


