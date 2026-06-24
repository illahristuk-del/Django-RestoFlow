from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_delete = 'django.db.models.BigAutoField'
    name = 'menu'

    def ready(self):
        import menu.signals