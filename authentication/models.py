from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default = False)
    otp = models.CharField(max_length=4, null=True, blank = True)
    forget_password_otp = models.CharField(max_length=4, null=True, blank = True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def name(self):
        return f'{self.first_name} {self.last_name}'

class ForgotPassword(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    forgot_password_otp = models.CharField(max_length=4, null = True, blank = True)
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.user.email