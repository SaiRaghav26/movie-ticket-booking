from .models import Seat

class SeatCreator:
    def __init__(self,show):
        self.show=show
        self.rows=show.rows
        self.columns=show.columns

    def create_seats(self):
        seats=[]
        for row in range(1,self.rows+1):
            for col in range(1,self.columns+1):
                seats.append(
                    Seat(
                        show=self.show,
                        is_booked=False
                    )
                    )
        #bulk create seats in database
        Seat.objects.bulk_create(seats)

    def run(self):
        self.create_seats()


    
