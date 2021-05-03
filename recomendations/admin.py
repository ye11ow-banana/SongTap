from django.contrib import admin
from .models import MusicUserToken


@admin.register(MusicUserToken)
class MusicUserTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'music_user_token']