from django.urls import path
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .views import HomePageView,ShowTimingPageView,TicketBookingPageView,LoginPageView,SignupPageView,ForgotPasswordPageView,ConfirmBookingPageView

urlpatterns=[
    path('',HomePageView.as_view(),name='home'),
    path('theatres/', ShowTimingPageView.as_view(), name='show_timings'),
    path('book_ticket/', TicketBookingPageView.as_view(), name='book_ticket'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('forgot-password/', ForgotPasswordPageView.as_view(), name='forgot-password'),
    path('confirm-booking/', ConfirmBookingPageView.as_view(), name='confirm-booking'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)