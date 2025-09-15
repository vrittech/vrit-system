from django.apps import AppConfig

class TeammemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teammember'

    def ready(self):
        # Import signals to ensure they are registered
        import teammember.signals