from django import forms
from django.contrib import admin
from .models import Movie,Theatre,Screen,ShowTimings,Seat
from .forms import SeatAdminForm

# Register your models here.
admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Screen)
admin.site.register(ShowTimings)

class SeatAdmin(admin.ModelAdmin):
    form=SeatAdminForm

admin.site.register(Seat,SeatAdmin)
