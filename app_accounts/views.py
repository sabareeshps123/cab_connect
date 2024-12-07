from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignUpSerializer, LoginSerializer, DriverProfileSerializer
from django.contrib.auth import authenticate


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            print("username",username)
            password = serializer.validated_data['password']
            print('password',password)
            user = authenticate(username=username, password=password)
            print('user_authenti',user)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            print('final')
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DriverProfileCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.user_type != 'driver':
            return Response({'error': 'Only drivers can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)

        serializer = DriverProfileSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            driver_profile = serializer.save()
            return Response(DriverProfileSerializer(driver_profile).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



