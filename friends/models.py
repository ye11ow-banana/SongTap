from django.db import models
from accounts.models import AppUser


class Friend(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user')
    friend = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name='Друг', related_name='friend')

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
