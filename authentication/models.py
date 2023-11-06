from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class BaseUser(BaseUserManager):
    def create_user(self, username=None,email=None,password=None,**extra_fields):
        if not username:
            raise ValueError('Username should not be None')
        
        user = self.model(username=username, email=self.normalize_email(email),)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user=self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class BetaUser(AbstractBaseUser, PermissionsMixin):
    profile=models.ImageField(upload_to='profile/',default='profile/default.svg')
    Note=models.CharField(max_length=50,blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=255)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)

    objects = BaseUser()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perm(self, app_label):
        return True
