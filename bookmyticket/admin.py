from django.contrib import admin
from .models import Movie,Theatre,Screen,ShowTimings,Seat

# Register your models here.
admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Screen)
admin.site.register(ShowTimings)
admin.site.register(Seat)
