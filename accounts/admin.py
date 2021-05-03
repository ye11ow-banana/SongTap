from django.contrib import admin
from .models import AppUser, InviteCode


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'apple_id', 'username']


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ['invite_code',]
