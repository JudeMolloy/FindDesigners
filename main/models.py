from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, username, display_name=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not display_name:
            display_name = username

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            display_name=display_name,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, display_name, password):
        user = self.create_user(
            email,
            username,
            display_name,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Designer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    display_name = models.CharField(max_length=25)
    twitter = models.CharField(max_length=15)
    bio = models.TextField(max_length=145, blank=True, default="")
    avatar = models.ImageField(upload_to='avatars', default='img/default_profile_pic.jpg')
    up_votes = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    thumbnail_price = models.FloatField()
    channel_art_price = models.FloatField()
    monthly = models.BooleanField(default=False)
    promoted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name", "username"]

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.display_name

    def get_long_name(self):
        return "{} (@{})".format(self.display_name, self.username)

    def is_available(self):
        if self.available:
            return '{} is available to work.'.format(self.display_name)
        else:
            return '{} is not available to work.'.format(self.display_name)

    def is_monthly(self):
        if self.monthly:
            return '{} does monthly deals.'.format(self.display_name)
        else:
            return '{} does not do monthly deals.'.format(self.display_name)

# class Designer(models.Model):
#     avatar = models.ImageField(upload_to='img/', default='img/default_profile_pic.jpg')
#     name = models.CharField(max_length=25)
#     twitter = models.CharField(max_length=15)
#     up_votes = models.IntegerField(default=0)
#     available = models.BooleanField(default=False)
#     thumbnail_price = models.FloatField()
#     channel_art_price = models.FloatField()
#     monthly = models.BooleanField(default=False)
#
#     # TIMEZONES =(
#     # )
#     # timezone = models.CharField(max_length=1, choices=TIMEZONES)
#     promoted = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.name
#
#     def is_available(self):
#         if self.available:
#             return '{} is available to work.'.format(self.name)
#         else:
#             return '{} is not available to work.'.format(self.name)
#
#     def is_monthly(self):
#         if self.monthly:
#             return '{} does monthly deals.'.format(self.name)
#         else:
#             return '{} does not do monthly deals.'.format(self.name)



