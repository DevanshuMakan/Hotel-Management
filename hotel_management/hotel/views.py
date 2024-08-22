from django.contrib import messages
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer
from .services import *


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

def home(request):
    return render(request, 'home.html')

def user_account(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'user_account.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('user_account')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


@login_required
def user_details(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'user_details.html', {'reservations': reservations})



def book_room(request):
    if request.method == 'POST':
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        room_type = request.POST.get('room_type')
        guests = request.POST.get('guests')
        special_requests = request.POST.get('special_requests')

        # Create a new booking instance and save it
        booking = Booking(
            user=request.user,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            room_type=room_type,
            guests=guests,
            special_requests=special_requests
        )
        booking.save()

        messages.success(request, 'Your room has been booked successfully!')
        return redirect('user_account')  # Redirect to the user account page where bookings are displayed

    return render(request, 'book_room.html')


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('user_details')
    return render(request, 'cancel_reservation.html', {'reservation': reservation})

def room_availability(request):
    if request.method == 'POST':
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        location = request.POST.get('location')

        availability = get_room_availability(checkin_date, checkout_date, location)

        return render(request, 'hotel/room_availability.html', {'availability': availability})

    return render(request, 'hotel/room_availability.html')
