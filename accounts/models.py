from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


# Create your models here.
# class User(models.Model):
#     first_name = models.CharField(max_length=200)
#     last_name = models.CharField(max_length=200)
#     username = models.CharField(max_length=200)
#     password = models.CharField(max_length=20)
#     email = models.EmailField(max_length=200)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.username

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the  given email and password
        :param email:
        :param password:
        :return:
        """

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password
        :param email:
        :param password:
        :return:
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin =True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(max_length=150, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, Always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        # Simplest possible answer: Yes: Always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
