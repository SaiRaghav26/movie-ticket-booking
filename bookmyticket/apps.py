from django.apps import AppConfig


class BookmyticketConfig(AppConfig):
    name = 'bookmyticket'

    def ready(self):
        import bookmyticket.signals
