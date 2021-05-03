from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _



class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('AppUsers')

