from django.apps import AppConfig


class GlassbricksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'glassbricks'

    def ready(self):
        import glassbricks.signals