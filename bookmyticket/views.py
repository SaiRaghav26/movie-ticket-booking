from django.http import Http404,JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import SignupForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView,CreateView,FormView
from django.contrib.auth.views import LoginView,PasswordResetView
from .models import Movie,ShowTimings,Seat,Screen,SeatCategory
from .serializer import MovieSerializer,ShowTimingsSerializer
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic.edit import FormView

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

    
class TicketBookingPageView(TemplateView):
    template_name = 'bookmyticket/ticket_booking.html'

    def get_context_data(self, **kwargs):
        movie_name = self.request.GET.get('movie', '').strip()
        theatre_name = self.request.GET.get('theatre', '').strip()
        screen = self.request.GET.get('screen', '').strip()
        time = self.request.GET.get('time', '').strip()
        date = self.request.GET.get('date', '').strip()

        context = super().get_context_data(**kwargs)

        # Start with all seats
        seat_query_set = Seat.objects.all()

        # Filter seats based on provided parameters
        if movie_name:
            screens = Screen.objects.filter(theatre__movies__title__icontains=movie_name)
            seat_query_set = seat_query_set.filter(screen__in=screens)

        if theatre_name or screen:
            screens = Screen.objects.all()
            if theatre_name:
                screens = screens.filter(theatre__theatre_name__icontains=theatre_name)
            if screen:
                screens = screens.filter(screen_number__icontains=screen)
            seat_query_set = seat_query_set.filter(screen__in=screens)

        if time or date:
            show_timings = ShowTimings.objects.all()
            if time:
                show_timings = show_timings.filter(show_time__icontains=time)
            if date:
                show_timings = show_timings.filter(date=date)
            screens = Screen.objects.filter(show_timings__in=show_timings)
            seat_query_set = seat_query_set.filter(screen__in=screens)

        # Categorize seats
        recliner_seats = seat_query_set.filter(seat_category__category_name='Recliner')
        executive_seats = seat_query_set.filter(seat_category__category_name='Executive')

        # Format time
        formatted_time = time
        if time:
            try:
                formatted_time = datetime.strptime(time, "%H:%M").strftime("%I:%M %p")
            except ValueError:
                formatted_time = time

        # Add required context
        context.update({
            'formatted_time': formatted_time,
            'movie_name': movie_name,
            'recliner_seats': recliner_seats,
            'executive_seats': executive_seats,
            'date': date,
            'theatre_name': theatre_name,
            'screen': screen
        })

        # Store selected seat details in session if POST request
        if self.request.method == 'POST':
            selected_seats = self.request.POST.get('selected_seats')
            total_price = self.request.POST.get('total_price')

            # Save session data: Only essential data
            self.request.session['selected_seats'] = selected_seats
            self.request.session['total_price'] = total_price

            # Optionally, store additional data like movie name, theatre, date, etc.
            self.request.session['movie_name'] = movie_name
            self.request.session['theatre_name'] = theatre_name
            self.request.session['screen'] = screen
            self.request.session['time'] = time
            self.request.session['date'] = date

            if self.request.user.is_authenticated:
                self.request.session['username'] = self.request.user.username

            # Redirect to confirm booking page
            return redirect('confirm-booking')

        return context



class LoginPageView(LoginView):
    template_name='bookmyticket/login.html'

    def form_valid(self,form):
        user = form.get_user()
        messages.success(self.request, 'Login successful')
        # self.request.session.save()  #  Force session to be saved
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request,'Invalid username or password')
        super().form_invalid(form)

class SignupPageView(FormView):
    form_class = SignupForm
    template_name='signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        user=form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, "Signup successful! Please log in.")
        return super().form_valid(form)
    
    def form_invalid(self,form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)




class ForgotPasswordPageView(PasswordResetView):
    template_name = 'bookmyticket/forgot_password.html'  # Custom template for the form
    email_template_name = 'bookmyticket/password_reset_email.html'  # Email template
    subject_template_name = 'bookmyticket/password_reset_subject.txt'  # Subject line template
    success_url = reverse_lazy('login')


class ConfirmBookingPageView(TemplateView):
    template_name = 'bookmyticket/confirm_booking.html'

    def get(self, request, *args, **kwargs):
        # Fetch data from session
        selected_seats = request.session.get('selected_seats', [])
        total_price = request.session.get('total_price', 0)
        movie_name = request.session.get('movie_name', '')
        theatre_name = request.session.get('theatre_name', '')
        screen = request.session.get('screen', '')
        time = request.session.get('time', '')
        date = request.session.get('date', '')

        context = {
            'selected_seats': selected_seats,
            'total_price': total_price,
            'movie_name': movie_name,
            'theatre_name': theatre_name,
            'screen': screen,
            'time': time,
            'date': date,
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # Handle the confirmation logic here, such as booking the seats
        # You can save the booking to the database and then redirect or display a success message
        # For example, save the booking to the database:
        
        # Assuming you have a Booking model
        # booking = Booking.objects.create(
        #     user=request.user,
        #     selected_seats=selected_seats,  # Make sure to parse and store selected seats correctly
        #     total_price=total_price,
        #     movie_name=movie_name,
        #     theatre_name=theatre_name,
        #     screen=screen,
        #     time=time,
        #     date=date,
        # )

        # Redirect to a confirmation or success page
        return redirect('confirm-booking')


    

    


        


    


    



    


    
    
        



