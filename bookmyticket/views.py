from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView,View,DetailView
from .models import Movie,ShowTimings,Seat
from .serializer import MovieSerializer,ShowTimingsSerializer,SeatSerializer
from datetime import datetime
from .forms import SeatAdminForm
from .utils import SeatCreator

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

    
class TicketBookingView(View):

    def get(self, request, *args, **kwargs):
        # Get query parameters
        movie = request.GET.get('movie')
        theatre = request.GET.get('theatre')
        screen = request.GET.get('screen')
        time = request.GET.get('time')
        date = request.GET.get('date')

        # Validate required parameters
        if not all([movie, theatre, screen, time, date]):
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        # Find the show using the parameters
        try:
            show = ShowTimings.objects.get(
                movie__title=movie,
                screen__theatre__theatre_name=theatre,
                screen__screen_number=screen,
                show_time=time,
                date=date,
            )
        except ShowTimings.DoesNotExist:
            return JsonResponse({'error': 'Show not found'}, status=404)

        # Get seats for the show
        seats = Seat.objects.filter(show=show)
        form=SeatAdminForm(show=show)
        
        #pass data to the template
        return render(request,'bookmyticket/ticket_booking.html',{
            'show':show,
            'seats':seats,
            'form':form,

        })
        


    



    


    
    
        



