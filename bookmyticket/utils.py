from .models import Seat,SeatCategory

class SeatCreator:
    def __init__(self,screen):
        self.screen=screen
        self.rows=screen.rows
        self.columns=screen.columns

    def get_seat_category(self,row):
        categories=SeatCategory.objects.filter(
            row_start__lte=row,
            row_end__gte=row
        ).filter(
            screen__screen_number=self.screen.screen_number,
            screen__theatre__theatre_name=self.screen.theatre.theatre_name
        )
        if categories.exists():
            category=categories.first()
            return category,category.price
        return None,None


    def create_seats(self):
        seats=[]
        for row in range(1,self.rows+1):
            seat_category,price=self.get_seat_category(row)
            if seat_category:
               for col in range(1,self.columns+1):
                  seat_number=f'{chr(64+row)}{col}'
                  if not Seat.objects.filter(screen=self.screen,seat_number=seat_number).exists():
                     seats.append(
                         Seat(
                        screen=self.screen,
                        seat_number=seat_number,
                        seat_category=seat_category,
                        price=price,
                        is_booked=False
                         )
                     )
        #bulk create seats in database
        Seat.objects.bulk_create(seats)

    def run(self):
        self.create_seats()


    
