from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Authentication'

           
    # def ready(self):
    #     from .signals import create_default_groups
    #     post_migrate.connect(create_default_groups, sender=self)
    
