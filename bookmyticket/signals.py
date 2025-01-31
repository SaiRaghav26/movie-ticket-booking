from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SeatCategory
from .utils import SeatCreator

class SeatSignalHandler:
    @staticmethod
    @receiver(post_save, sender=SeatCategory)
    def create_seats(sender, instance, created, **kwargs):
        # Trigger only if the SeatCategory is newly created and has a valid screen
        if created and instance.screen:
            screen = instance.screen
            # Create seats for the newly created SeatCategory and its associated screen
            seat_creator = SeatCreator(screen)
            seat_creator.run()  # Create seats using seat creator utility
            print(f'Seats created for the screen: {screen}')
        elif instance.screen:
            # You can also trigger when an existing SeatCategory is updated with a valid screen
            print(f'Seats creation triggered for screen: {instance.screen}, but no new category created.')
