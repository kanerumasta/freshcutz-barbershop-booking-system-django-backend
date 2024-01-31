from django.db import models
from djongo import models
from authentication.models import User
from django.db.models import Sum
from django.core.exceptions import ValidationError
import random

class DisabledDate(models.Model):
    date = models.DateField()
    reason = models.TextField(blank = True, null = True)


class Time(models.Model):
    time = models.TimeField()
    max_capacity = models.IntegerField(default = 1)


class Barber(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)



class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True) 
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class Style(models.Model):
    name = models.CharField(max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, related_name="styles")
    image = models.ImageField(upload_to='images', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"style {self.name} {self.id} of {self.service.name}  {self.service.id}"

class Booking(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
       
        ('completed', 'Completed'),
    )

    code = models.CharField(max_length = 7, unique=True, null=True)

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='BookingService', related_name='bookings')
    date = models.DateField()
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)
    rate = models.IntegerField(null=True, blank=True)
    total = models.FloatField( null=True, blank = True)

    def generate_random_code(self):
        return str(random.randint(1000000, 9999999))


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_random_code()
        super().save(*args, **kwargs)
            
       
class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    style = models.ForeignKey(Style,null=True,on_delete=models.CASCADE)

    class Meta:
        # Add a unique constraint for the combination of booking, service, and style
        unique_together = ['booking', 'service', 'style']

class Notification(models.Model):
    status = models.CharField(max_length = 10, default="pending", null=True)
    booking = models.ForeignKey(Booking, on_delete= models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    message = models.TextField()
    title = models.CharField(max_length = 255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True, null=True)

    