# hotel/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, RoomViewSet, BookingViewSet
from .views import *

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
]
