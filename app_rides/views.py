from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app_rides.serializers import RideSerializer,DriverLocationSerializer
from math import radians, cos, sin, sqrt, atan2
from app_rides.models import Driver, Ride
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut



class CreateRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RideSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            ride = serializer.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            ride = Ride.objects.get(id=pk)
            if ride.rider != request.user and ride.driver != request.user:
                return Response({"error": "You are not authorized to view this ride."}, status=status.HTTP_403_FORBIDDEN)
            return Response(RideSerializer(ride).data)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

class RideListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'rider':
            return Response({"error": "Only riders can view their rides."}, status=status.HTTP_403_FORBIDDEN)

        rides = Ride.objects.filter(rider=request.user)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)

class UpdateRideStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ride = Ride.objects.get(id=pk)
            if ride.driver != request.user.driver_profile:
                return Response({"error": "Only the driver can update the ride status."}, status=status.HTTP_403_FORBIDDEN)

            ride_status = request.data.get('status')
            if ride_status not in ['started', 'completed', 'accepted', 'cancelled']:
                return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

            ride.status = ride_status
            ride.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

class CancelRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            ride = Ride.objects.get(id=pk)
            if ride.rider != request.user:
                return Response({"error": "Only the rider can cancel the ride."}, status=status.HTTP_403_FORBIDDEN)

            ride.status = 'cancelled'
            ride.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_200_OK)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

class UpdateDriverLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print('uu', request.user.user_type)
        if request.user.user_type != 'driver':
            return Response({"error": "Only drivers can update their location."}, status=status.HTTP_403_FORBIDDEN)

        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        driver = request.user.driver_profile
        driver.latitude = latitude
        driver.longitude = longitude
        driver.save()
        return Response({"message": "Driver location updated successfully."}, status=status.HTTP_200_OK)



class NearbyRidesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'driver':
            return Response({"error": "Only drivers can view nearby rides."}, status=status.HTTP_403_FORBIDDEN)

        driver = request.user.driver_profile
        driver_latitude = driver.latitude
        driver_longitude = driver.longitude

        nearby_rides = Ride.objects.filter(status='pending').order_by('created_at')

        geolocator = Nominatim(user_agent="app_rides")

        rides_within_radius = []
        for ride in nearby_rides:
            distance_km = self.calculate_distance(driver_latitude, driver_longitude, ride.pickup_latitude,
                                                  ride.pickup_longitude)
            if distance_km <= 50:
                serialized_ride = RideSerializer(ride).data
                serialized_ride['distance_km'] = round(distance_km, 2)

                pickup_address = self.get_address(ride.pickup_latitude, ride.pickup_longitude, geolocator)
                dropoff_address = self.get_address(ride.dropoff_latitude, ride.dropoff_longitude, geolocator)

                serialized_ride['pickup_location'] = pickup_address
                serialized_ride['dropoff_location'] = dropoff_address

                rides_within_radius.append(serialized_ride)

        return Response(rides_within_radius)

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great-circle distance between two points on the Earth (specified in decimal degrees).
        Returns the distance in kilometers.
        """
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius_of_earth_km = 6371
        return radius_of_earth_km * c

    @staticmethod
    def get_address(latitude, longitude, geolocator):
        """
        Given a latitude and longitude, return the address using geopy's Nominatim service.
        """
        try:
            location = geolocator.reverse((latitude, longitude), language="en", timeout=10)
            return location.address if location else "Address not found"
        except GeocoderTimedOut:
            return "Geocoder service timed out"
        except Exception as e:
            return f"Error: {str(e)}"







class NearbyDriversView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'rider':
            return Response({"error": "Only riders can view nearby drivers."}, status=status.HTTP_403_FORBIDDEN)

        try:
            active_ride = Ride.objects.filter(rider=request.user, status='pending').first()
            if not active_ride:
                return Response({"error": "No active ride found for the rider."}, status=status.HTTP_404_NOT_FOUND)
        except Ride.DoesNotExist:
            return Response({"error": "No active ride found for the rider."}, status=status.HTTP_404_NOT_FOUND)

        pickup_latitude = active_ride.pickup_latitude
        pickup_longitude = active_ride.pickup_longitude
        drivers = Driver.objects.all()
        geolocator = Nominatim(user_agent="app_rides")
        drivers_within_radius = []

        for driver in drivers:
            if driver.latitude and driver.longitude:
                distance_km = self.calculate_distance(
                    pickup_latitude, pickup_longitude, driver.latitude, driver.longitude
                )
                if distance_km <= 50:
                    driver_data = DriverLocationSerializer(driver).data
                    driver_data['distance_km'] = round(distance_km, 2)

                    driver_location = self.get_address(driver.latitude, driver.longitude, geolocator)
                    driver_data['location'] = driver_location

                    drivers_within_radius.append(driver_data)

        return Response(drivers_within_radius, status=status.HTTP_200_OK)

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        radius_of_earth_km = 6371
        return radius_of_earth_km * c

    @staticmethod
    def get_address(latitude, longitude, geolocator):
        try:
            location = geolocator.reverse((latitude, longitude), language="en", timeout=10)
            return location.address if location else "Address not found"
        except GeocoderTimedOut:
            return "Geocoder service timed out"
        except Exception as e:
            return f"Error: {str(e)}"