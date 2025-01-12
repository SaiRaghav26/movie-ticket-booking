from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomePageView,ShowTimingPageView,TicketBookingView

urlpatterns=[
    path('',HomePageView.as_view(),name='home'),
    path('theatres/', ShowTimingPageView.as_view(), name='show_timings'),
    path('book_ticket/', TicketBookingView.as_view(), name='book_ticket'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)