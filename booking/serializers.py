from rest_framework import serializers
from .models import *

class BarberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barber
        fields = '__all__'

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    styles = StyleSerializer(many=True, read_only=True)
    class Meta:
        model = Service
        fields = '__all__'

class TimeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Time
        fields = '__all__'

class DisabledDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabledDate
        fields='__all__'


class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = '__all__'

class BookingServiceSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = BookingService
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['service'] = ServiceSerializer()
        self.fields['style'] = StyleSerializer()
        return super().to_representation(instance)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


