
from django.urls import path
from .views import (
    CreateRideView,
    RideDetailView,
    RideListView,
    UpdateRideStatusView,
    CancelRideView,
    UpdateDriverLocationView,
    NearbyRidesView,
    NearbyDriversView,
)

urlpatterns = [
    path('create/', CreateRideView.as_view(), name='create_ride'),
    path('ride/<int:pk>/', RideDetailView.as_view(), name='ride_detail'),
    path('rides/', RideListView.as_view(), name='ride_list'),
    path('ride/<int:pk>/status/', UpdateRideStatusView.as_view(), name='update_ride_status'),
    path('ride/<int:pk>/cancel/', CancelRideView.as_view(), name='cancel_ride'),
    path('driver-location/', UpdateDriverLocationView.as_view(), name='update_driver_location'),
    path('nearby-rides/', NearbyRidesView.as_view(), name='nearby_rides'),
    path('nearby-drivers/', NearbyDriversView.as_view(), name='nearby-drivers'),
]

