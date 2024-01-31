from django.contrib import admin
from .models import *

admin.site.register([Service, Booking, Style, Barber,BookingService,DisabledDate, Notification])

