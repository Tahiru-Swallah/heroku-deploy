from django.shortcuts import render
from .models import Profile, CustomUser
from .serializers import CreateCustomUserSerializer, LoginSerializer, PasswordChangeSerializer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.reverse import reverse

class MyPublicView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        data = {"message": "This view is accessible to anyone."}
        return Response(data)

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)

            return Response(
                {
                    'token': token.key,
                    'user': {
                        'email': user.email,
                        'phone_number': user.phone_number,
                    }
                }, status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class Api_Root(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({
            'login': reverse('login_api', request=request),
            'register': reverse('signup_api', request=request),
            'my_public': reverse('mypublicapi', request=request),
            'change_password': reverse('change_password_api', request=request)
        })

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail":"Password change successfully"},
                status = status.HTTP_200_OK
            )
        
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )