from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from allotments.models import Branch
from datetime import datetime
# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username=None
    email=models.EmailField(max_length=50,unique=True)
    is_faculty=models.BooleanField(default=True)
    is_hod=models.BooleanField(default=False)
    is_exam_section=models.BooleanField(default=False)
    faculty_branch=models.ForeignKey(Branch,on_delete=models.SET_NULL,related_name='faculty_branch',null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','password']
    date_joined=None
    objects = UserManager()
    def __str__(self):
        return self.first_name+" "+self.last_name