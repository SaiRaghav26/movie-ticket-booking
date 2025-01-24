from .models import Seat,SeatCategory

class SeatCreator:
    def __init__(self,show):
        self.show=show
        self.rows=show.screen.rows
        self.columns=show.screen.columns

    def get_seat_category(self,row):
        categories=SeatCategory.objects.filter(
            row_start__lte=row,
            row_end__gte=row
        ).filter(
            screen__screen_number=self.show.screen.screen_number,
            screen__theatre__theatre_name=self.show.screen.theatre.theatre_name
        )
        if categories.exists():
            category=categories.first()
            return category,category.price
        return None,None


    def create_seats(self):
        seats=[]
        for row in range(1,self.rows+1):
            for col in range(1,self.columns+1):
                seat_number=f'{chr(64+row)}{col}'
                seat_category,price=self.get_seat_category(row)
                seats.append(
                    Seat(
                        show=self.show,
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


    
