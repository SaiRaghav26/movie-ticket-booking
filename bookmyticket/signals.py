from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Seat,ShowTimings
from .utils import SeatCreator


class SeatSignalHandler:
    @staticmethod
    @receiver(post_save,sender=ShowTimings)

    def create_seats(sender,instance,created,**kwargs):
        if created:
            #create seats for the newly created instance
            seat_creator=SeatCreator(instance)
            seat_creator.run()#create seats using seat creator utility
            print(f'seats created for the show{instance.movie}')




