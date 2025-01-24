from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Movie,ShowTimings,Seat,Screen,SeatCategory
from .serializer import MovieSerializer,ShowTimingsSerializer
from datetime import datetime
from .forms import SeatAdminForm

class HomePageView(TemplateView):
    template_name='bookmyticket/home.html'

    def get_context_data(self, **kwargs):
        #retrive data from database
        movies=Movie.objects.all()
        #serialize the data
        serializer=MovieSerializer(movies,many=True)
        #add serialized data to the context
        context=super().get_context_data(**kwargs)
        context['movies']=serializer.data
        return context
    

from datetime import datetime

class ShowTimingPageView(TemplateView):
    template_name = 'bookmyticket/theatres.html'
    
    def get_context_data(self, **kwargs):
        # Get the movie_name from the query parameters
        movie_name = self.request.GET.get('movie', '').strip()
        
        # If no movie_name is provided, raise an error (display a friendly message)
        if not movie_name:
            raise Http404("Movie name is required")

        # Fetch the specific movie
        movie = get_object_or_404(Movie, title__iexact=movie_name)
        
        # Get today's date
        today = datetime.today().date()
        
        # Default date logic
        movie_release_date = movie.release_date
        default_date = today if movie_release_date <= today else movie_release_date
        
        # Fetch all available dates for the movie
        available_dates = ShowTimings.objects.filter(movie=movie).values('date').distinct()
        
        # Get selected date from GET request, default to calculated default date
        selected_date = self.request.GET.get('date', str(default_date))
        
        # Ensure the selected_date is in the correct format (YYYY-MM-DD)
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            # If there was an issue with the format, use the default date
            selected_date = default_date
        
        # Fetch show timings for the selected date
        show_timings = ShowTimings.objects.filter(movie=movie, date=selected_date)
        
        # Serialize the show timings
        serializer = ShowTimingsSerializer(show_timings, many=True)
        
        # Add data to the context
        context = super().get_context_data(**kwargs)
        context['show_timings'] = serializer.data
        context['movie'] = movie  # Pass the movie details
        context['available_dates'] = available_dates  # Pass the available dates
        context['selected_date'] = selected_date  # Pass the selected date
        
        return context

    
class TicketBookingView(TemplateView):
    template_name = 'bookmyticket/ticket_booking.html'

    def get_context_data(self, **kwargs):
        movie_name = self.request.GET.get('movie', '').strip()
        theatre_name = self.request.GET.get('theatre', '').strip()
        screen = self.request.GET.get('screen', '').strip()
        time = self.request.GET.get('time', '').strip()
        date = self.request.GET.get('date', '').strip()

        context = super().get_context_data(**kwargs)
        
        seat_query_set = Seat.objects.all()

        if movie_name:
            show_timings = ShowTimings.objects.filter(movie__title__icontains=movie_name)
            seat_query_set = seat_query_set.filter(show__in=show_timings)

        if theatre_name or screen:
            screens = Screen.objects.all()
            if theatre_name:
                screens = screens.filter(theatre__theatre_name__icontains=theatre_name)

            if screen:
                screens = screens.filter(screen_number__icontains=screen)

            seat_query_set = seat_query_set.filter(show__screen__in=screens)

        if time:
            seat_query_set = seat_query_set.filter(show__show_time__icontains=time)

        if date:
            seat_query_set = seat_query_set.filter(show__date=date)

        # Categorize seats
        recliner_seats = seat_query_set.filter(seat_category__category_name='Recliners')  # Rows A and B
        executive_seats = seat_query_set.exclude(seat_category__category_name='Executive')  # All other rows

        # Pass categorized seats to the context
        context['recliner_seats'] = recliner_seats
        context['executive_seats'] = executive_seats
        return context


        


    


    



    


    
    
        



