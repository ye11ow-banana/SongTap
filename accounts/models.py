from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class AppUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Man'),
        ('W', 'Woman'),
    )

    username = models.CharField(verbose_name='Username', unique=True, max_length=50)
    email = models.CharField(verbose_name='E-mail', unique=True, max_length=50, blank=True, null=True)
    apple_id = models.CharField(verbose_name='Apple ID', unique=True, max_length=200)
    gender = models.CharField(verbose_name='Gender', choices=GENDER_CHOICES, blank=True, null=True, max_length=1)
    age = models.CharField(verbose_name='Age', blank=True, null=True, max_length=10)

    photo = models.ImageField(
        upload_to='accounts', blank=True, null=True,
        default='accounts/default.jpg'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        if self.email:
            return self.email
        elif self.username:
            return self.username
        else:
            return self.apple_id


class InviteCode(models.Model):
    invite_code = models.CharField(verbose_name='Invite code', unique=True, max_length=500)

    class Meta:
        verbose_name = 'Инвайт код'
        verbose_name_plural = 'Инвайт коды'
