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
    room_number = models.CharField(max_length=5)
    room_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2,null=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f'Room {self.room_number} - {self.room_type}'

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'Reservation by {self.user.username} for {self.room.room_number}'

class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f'{self.user.username} booking for room {self.room.room_number}'