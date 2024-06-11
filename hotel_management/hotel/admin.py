from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price', 'availability')
    list_filter = ('room_type', 'availability')
    search_fields = ('room_number', 'room_type')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out')
    list_filter = ('check_in', 'check_out')
    search_fields = ('user__username', 'room__room_number')
