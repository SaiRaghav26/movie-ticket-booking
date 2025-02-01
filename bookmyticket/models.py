from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Movie(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    release_date=models.DateField(default=datetime.date.today)
    genre=models.CharField(max_length=50)
    runtime=models.IntegerField(help_text='Runtime in minutes')
    posters=models.ImageField(upload_to='posters/',default='movies/kill.JPG')
    banners=models.ImageField(upload_to='banners/',blank=True,null=True)

    def __str__(self):
        return self.title
    
class Theatre(models.Model):
    theatre_name=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    movies=models.ManyToManyField(Movie,related_name='theatres')

    def __str__(self):
        return f'{self.theatre_name} in {self.location}'
    
class Screen(models.Model):
    theatre=models.ForeignKey(Theatre,related_name='screens',on_delete=models.CASCADE)
    screen_number=models.IntegerField()
    rows = models.IntegerField(default=12)  # Define the number of rows for the show
    columns = models.IntegerField(default=12)

    def __str__(self):
        return f'{self.screen_number} in {self.theatre.theatre_name}'
    
class SeatCategory(models.Model):
    #creates seat category for each screen like VIP,executive etc
    screen=models.ForeignKey(Screen,related_name='seat_category',on_delete=models.CASCADE)
    category_name=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    row_start=models.IntegerField()
    row_end=models.IntegerField()

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['screen','category_name'],
                name='unique_seat_category_per_screen'
            )
        ]
    def __str__(self):
        return f'{self.category_name} ({self.row_start}-{self.row_end}) -{self.screen.theatre.theatre_name} - Screen{self.screen.screen_number}'

    

class ShowTimings(models.Model):
    theatre=models.ForeignKey(Theatre,related_name='show_timings',on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,related_name='show_timings',on_delete=models.CASCADE)
    show_time=models.TimeField()
    screen=models.ForeignKey(Screen,related_name='show_timings',on_delete=models.CASCADE)
    date=models.DateField(default=datetime.date.today)

    class Meta:
        constraints=[
            models.UniqueConstraint(
            fields=['theatre','screen','show_time','date'],
            name='unique_show_time_per_screen'
            )
        ]
    
    def formatted_time(self):
        return self.show_time.strftime("%I:%M %p")
    
    def __str__(self):
        return f'{self.movie.title} at {self.show_time} in screen:{self.screen.screen_number} on {self.date} in {self.theatre.theatre_name},{self.theatre.location}'
    

class Seat(models.Model):
    screen = models.ForeignKey(Screen, related_name='seats', on_delete=models.CASCADE)
    seat_number=models.CharField(max_length=10)
    seat_category = models.ForeignKey(SeatCategory, related_name="seats", on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=6,decimal_places=2,default=None)
    is_booked = models.BooleanField(default=False)  # Whether the seat is booked or not
    

    def __str__(self):
        return f'created {self.seat_number} -{self.seat_category.category_name} for  {self.screen.screen_number} at {self.screen.theatre.theatre_name}'
    

class ConfirmBooking(models.Model):
    user=models.ForeignKey(User,related_name='confirm_booking',on_delete=models.CASCADE)
    show=models.ForeignKey(ShowTimings,related_name='confirm_booking',on_delete=models.CASCADE,default=None)
    number_of_tickets=models.IntegerField(default=0)
    seat_numbers=models.CharField(max_length=500,null=True)
    price=models.DecimalField(max_digits=6,decimal_places=2,default=None)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} has booking to confirm for {self.show.movie.title} on {self.show.date}||{self.show.show_time} at {self.show.theatre.theatre_name} ,{self.show.theatre.location}'
    




    



    



