from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from .views import HomePageView,ShowTimingPageView,TicketBookingPageView,LoginPageView,SignupPageView,ForgotPasswordPageView

urlpatterns=[
    path('',HomePageView.as_view(),name='home'),
    path('theatres/', ShowTimingPageView.as_view(), name='show_timings'),
    path('book_ticket/', TicketBookingPageView.as_view(), name='book_ticket'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordPageView.as_view(template_name='bookmyticket/forgot_password.html'), name='forgot-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)