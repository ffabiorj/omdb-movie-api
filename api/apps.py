from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        import api.signals


# class UsersConfig(AppConfig):
#     name = "users"
#
#     def ready(self):
#         import api.signals
