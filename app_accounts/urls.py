from django.urls import path
from .views import SignUpView, LoginView, DriverProfileCreateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('driver-profile/', DriverProfileCreateView.as_view(), name='driver_profile'),
]
