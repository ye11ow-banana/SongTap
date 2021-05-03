from django.apps import AppConfig


class RecomendationsConfig(AppConfig):
    name = 'recomendations'

    def ready(self):
        import recomendations.signals
