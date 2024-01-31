from django.urls import path
from .views import *


urlpatterns = [
	path('bookings', BookingListAPIView.as_view(), name='booking-list'),
    	path('bookings/<int:pk>', BookingDetailAPIView.as_view(), name='booking-detail'),
            
	path('barbers', BarberListAPIView.as_view(), name='barber-list'),
    	path('barbers/<int:pk>', BarberDetailAPIView.as_view(), name='barber-detail'),
            
    	path('services', ServiceListCreateAPIView.as_view(), name='service-list'),
    	path('services/<int:pk>', ServiceRetrieveUpdateDestroyAPIView.as_view(), name='service-detail'),
            
    	path('styles', StyleListCreateAPIView.as_view(), name='style-list'),
    	path('styles/<int:pk>', StyleRetrieveUpdateDestroyAPIView.as_view(), name='style-detail'),
            
	path('booking-services', BookingServiceListCreateAPIView.as_view(), name = 'booking-service list'),
        path('booking-services/<int:pk>', BookingServiceRetrieveUpdateDestroyAPIView.as_view(), name = 'booking-service-detail'),
	
	path('time', TimeListCreateAPIView.as_view(), name = 'time-list'),
        path('time/<int:pk>', TimeRetrieveUpdateDestroyAPIView.as_view(), name = 'time-detail'),
	
	path('disabled-dates', DisableDateListCreateAPIView.as_view(), name = 'disabled-date-list'),
        path('disabled-dates/<int:pk>', DisableDateRetrieveUpdateDestroyAPIView.as_view(), name = 'disabled-date-detail'),

	path('get-booking-services/<int:booking_id>',get_booking_services_by_booking,name="get_booking_services_by_booking"),	
	path('is-time-taken', is_date_time_taken, name='is-time-taken'),
        
	path('confirm-booking', confirm_booking, name='confirm-booking'),
	path('complete-booking', booking_completed, name='booking-complete'),
	path('user-bookings', get_user_bookings, name='user-bookings'),
	path('user-notifications', get_notifications, name='user-notifications'),
	path('rate-booking', rate_booking, name='rate-booking'),
]