from django.db import models

# Create your models here.
# hotel/models.py

from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.room_number} - {self.room_type}'

class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f'{self.user.username} booking for room {self.room.room_number}'
