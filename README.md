# Ride Sharing Django Project

This is a Django project for a ride-sharing application where users can sign up as either a rider or a driver, create and manage ride requests, and update ride statuses. The project includes two main apps: **app_accounts** and **app_rides**.

## Table of Contents

- [Installation](#installation)
- [App Overview](#app-overview)
  - [app_accounts URLs](#app_accounts-urls)
  - [app_rides URLs](#app_rides-urls)
- [Additional Notes](#additional-notes)

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <project_directory>
```


2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate
```

3. Install the project dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```
The application will be running at http://127.0.0.1:8000/.


## App Overview

### app_accounts URLs

1. **`path('signup/', SignUpView.as_view(), name='signup')`**:
   - This URL is used for signing up both riders and drivers. The signup process requires basic details like user type (driver or rider) and other relevant information.

2. **`path('login/', LoginView.as_view(), name='login')`**:
   - This URL allows riders and drivers to log in using their credentials.

3. **`path('driver-profile/', DriverProfileCreateView.as_view(), name='driver_profile')`**:
   - This URL is used by a logged-in driver to create their profile, including additional details like locations, license, etc.

### app_rides URLs

1. **`path('create/', CreateRideView.as_view(), name='create_ride')`**:
   - This URL allows a logged-in rider to create a ride request. The rider provides details like pickup location, destination.

2. **`path('ride/<int:pk>/', RideDetailView.as_view(), name='ride_detail')`**:
   - This URL allows a logged-in rider to view the details of a particular ride request using the ride ID (primary key).

3. **`path('rides/', RideListView.as_view(), name='ride_list')`**:
   - This URL lists all ride requests for the logged-in rider.

4. **`path('ride/<int:pk>/status/', UpdateRideStatusView.as_view(), name='update_ride_status')`**:
   - This URL is used by drivers to update the status of a ride. Possible statuses include accepted, canceled, started, or completed.

5. **`path('ride/<int:pk>/cancel/', CancelRideView.as_view(), name='cancel_ride')`**:
   - This URL allows a logged-in rider to cancel a ride request.

6. **`path('driver-location/', UpdateDriverLocationView.as_view(), name='update_driver_location')`**:
   - This URL allows drivers to update their current location, helping the system track their position for nearby ride requests.

7. **`path('nearby-rides/', NearbyRidesView.as_view(), name='nearby_rides')`**:
   - This URL is used by logged-in drivers to view nearby ride requests from riders.

8. **`path('nearby-drivers/', NearbyDriversView.as_view(), name='nearby-drivers')`**:
   - This URL is used by logged-in riders to view nearby drivers who are available for rides.


## Additional Notes

- **Permissions**: Ensure that the user roles (riders and drivers) are correctly assigned and managed using Django's built-in user authentication system.
- **Admin Panel**: Use the Django admin panel to manage users, rides, and their statuses by navigating to `http://127.0.0.1:8000/admin/`.
