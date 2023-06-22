from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name,  email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not phone_number:
            raise ValueError('User must have a Phone number')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            # last_name = last_name,
            phone_number = phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, email, phone_number, password):
        user = self.create_user(
            email = self.normalize_email(email),
            phone_number = phone_number,
            password = password,
            first_name = first_name,
            # last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser,PermissionsMixin):
    # username = None
    first_name      = models.CharField(max_length=50)
    email           = models.EmailField(max_length=50, unique=True)
    phone_number    = models.CharField(max_length=10, unique=True)



    place_or_area = models.CharField(max_length=200,blank=True,null=True)
    block_number = models.CharField(max_length=200,blank=True,null=True)
    house_building_number = models.CharField(max_length=200,blank=True,null=True)
    street_avenue_number = models.TextField(blank=True,null=True)
    


    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['first_name', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email


    def full_name(self):
        return f'{self.first_name}'


    def has_perm(self, perm, obj=None):
        return self.is_admin


    def has_module_perms(self, add_label):
        return True