from django import forms
from django.contrib import admin
from .models import Movie,Theatre,Screen,ShowTimings,SeatCategory,Seat

# Register your models here.
admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Screen)
admin.site.register(SeatCategory)
admin.site.register(ShowTimings)

class SeatAdmin(admin.ModelAdmin):
    # Display the seat_number, show, seat_category, and is_booked
    list_display = ('seat_number', 'screen', 'seat_category', 'is_booked')  

    # Add filters for easier searching
    list_filter = ('screen', 'seat_category', 'is_booked')  

    # Enable search on seat_number and the associated movie title
    search_fields = ('seat_number', 'screen__theatre__movie__title')

admin.site.register(Seat, SeatAdmin)


