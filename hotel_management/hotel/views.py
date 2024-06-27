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
    return render(request, 'index.html')


def home(request):
    return render(request, 'index.html')


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
        form = ReservationForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']

            # Check if the room is available
            overlapping_reservations = Reservation.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in
            )
            if overlapping_reservations.exists():
                error_message = 'This room is already booked for the selected dates.'
                return render(request, 'book_room.html', {'form': form, 'error_message': error_message})

            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('user_details')
    else:
        form = ReservationForm()
    return render(request, 'book_room.html', {'form': form})


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('user_details')
    return render(request, 'cancel_reservation.html', {'reservation': reservation})
