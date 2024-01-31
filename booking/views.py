from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import status, generics


class BookingListAPIView(generics.ListCreateAPIView):
    queryset = Booking.objects.all().order_by('-created_at')
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        notification = { 'booking':booking.id,'user' : 1, 'message':'A new booking is awaiting confirmation.', 'title':f'New Pending Booking : {booking.code}' }
        serializer = NotificationSerializer(data = notification)
        if serializer.is_valid():
            serializer.save()

class BookingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    ordering_fields = ['date', 'time']
    ordering = ['-date', '-time']

class BarberListAPIView(generics.ListCreateAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class BarberDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Barber.objects.all()
    serializer_class = BarberSerializer

class ServiceTypeCreateAPIView(generics.CreateAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer

class ServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    
class StyleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer

class StyleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Style.objects.all()
    serializer_class = StyleSerializer


class BookingServiceListCreateAPIView(generics.ListCreateAPIView):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer

class BookingServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingService.objects.all()
    serializer_class = BookingServiceSerializer

class TimeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Time.objects.all().order_by('time')
    serializer_class = TimeSerializer
   


class TimeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Time.objects.all()
    serializer_class = TimeSerializer

class DisableDateListCreateAPIView(generics.ListCreateAPIView):
    queryset = DisabledDate.objects.all()
    serializer_class = DisabledDateSerializer

class DisableDateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DisabledDate.objects.all()
    serializer_class = DisabledDateSerializer

@api_view(['GET'])
def get_booking_services_by_booking(request, booking_id):
    try:
        booking_services = BookingService.objects.filter(booking=booking_id)
        serializer = BookingServiceSerializer(booking_services, many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    except:
        return Response({'message':'error getting booking services'},status = status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def is_date_time_taken(request):
    try:
        date = request.GET.get('date') 
        time = int(request.GET.get('time'))

        booking = Booking.objects.filter(date=date, time=time)
        if booking:
            taken = True
        else: 
            taken = False
        

        return Response({'is_taken': taken}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def confirm_booking(request):
    booking_id = request.data['booking_id']
    try:
        booking =   get_object_or_404(Booking, id = booking_id)
        booking.status = "confirmed"
        
        notification = get_object_or_404(Notification, booking=booking_id)
        notification.title = "Booking Confirmed"
        notification.message = f'Your booking {booking.code} has been confirmed'
        notification.user = booking.customer
        notification.save()
        booking.save()
      
        return Response({'message':'booking confirmed'}, status=status.HTTP_200_OK)
 
        
    except Booking.DoesNotExist:
        return Response({'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    except Notification.DoesNotExist:
        return Response({'message': 'Notification not found for the booking'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Handle other exceptions if needed
        return Response({'message': f'Error confirming booking: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def booking_completed(request):
    try:
        booking_id = request.data['booking_id']
        booking = get_object_or_404(Booking, id=booking_id)

        # Update booking status to "completed"
        booking.status = "completed"
        booking.save()

        # Update the related notification
        notification = get_object_or_404(Notification, booking=booking)
        notification.title = "Service Completed"
        notification.message = f'Your booking {booking.code} has been completed'
        notification.save()

        return Response({'message': 'Booking completed'}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({'message': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    except Notification.DoesNotExist:
        return Response({'message': 'Notification not found for the booking'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Handle other exceptions if needed
        return Response({'message': f'Error completing booking: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_bookings(request):
    user = request.GET.get('user')
    try:
        bookings = Booking.objects.filter(customer = user).order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        return Response({'message':'error getting bookings for the user'}, status  = status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_notifications(request):
    user = request.GET.get('user')
    try:
        notifications = Notification.objects.filter(user = user).exclude(status = "read").order_by('-created_at')
        serializer = NotificationSerializer(notifications, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    except:
        return Response({'message':'error getting notifications'}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def rate_booking(request):
    booking_id = request.data['booking_id']
    rate = request.data['rate']
    comment = request.data['comment']
    try:
        booking = get_object_or_404(Booking, id = booking_id)
        if(booking):
            booking.rate = rate
            booking.comment = comment
            booking.save()
            notif = get_object_or_404(Notification, booking=booking_id)
            if notif:
                notif.status = "read"
                notif.save()
            return Response({'message':'succesfully rated booking'}, status = status.HTTP_200_OK)
    except:

        return Response({'message':'ERROR'}, status = status.HTTP_400_BAD_REQUEST)