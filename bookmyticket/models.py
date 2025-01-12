from django.db import models
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

    def __str__(self):
        return f'{self.screen_number} in {self.theatre.theatre_name}'
    

class ShowTimings(models.Model):
    theatre=models.ForeignKey(Theatre,related_name='show_timings',on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,related_name='show_timings',on_delete=models.CASCADE)
    show_time=models.TimeField()
    screen=models.ForeignKey(Screen,related_name='show_timings',on_delete=models.CASCADE)
    date=models.DateField(default=datetime.date.today)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['theatre','screen','show_time','date'],name='unique_show_time_per_screen')
        ]

    def __str__(self):
        return f'{self.movie.title} at {self.show_time} in screen:{self.screen.screen_number} on {self.date} in {self.theatre.theatre_name},{self.theatre.location}'
    

class Seat(models.Model):
    show = models.ForeignKey(ShowTimings, related_name='seats', on_delete=models.CASCADE)
    row = models.CharField(max_length=2)  # A, B, C, ...
    column = models.IntegerField()  # 1, 2, 3, ...
    is_booked = models.BooleanField(default=False)  # Whether the seat is booked or not

    class Meta:
        unique_together = ('show', 'row', 'column')

    def __str__(self):
        return f'{self.row}{self.column} in {self.show.screen.screen_number} at {self.show.date}'
    



    



