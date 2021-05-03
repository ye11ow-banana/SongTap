from django.db import models
from django.conf import settings


class MusicUserToken(models.Model):
    '''Юзер токен для Apple Music API'''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    music_user_token = models.CharField(
        verbose_name='Токен', max_length=2000
    )