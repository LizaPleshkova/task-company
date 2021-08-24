from rest_framework import routers
from django.urls import path, include

from .views import (
    PlaceView,
    RoomView,
    OfficeView, BookingPlaceView
)

router = routers.SimpleRouter()

router.register(r'booking-place', BookingPlaceView, basename='booking_place')
router.register(r'places', PlaceView, basename='places')
router.register(r'rooms', RoomView, basename='rooms')
router.register(r'offices', OfficeView, basename='offices')

urlpatterns = [
    path('', include(router.urls)),
]
