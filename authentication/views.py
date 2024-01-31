from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from .models import User
from rest_framework import status, generics
from rest_framework import serializers
from django.db import IntegrityError, DatabaseError
from rest_framework.decorators import api_view
from .utils import *


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def validate(self, attrs):
        data = super().validate(attrs)

    
        user = self.user
        data['is_verified'] = user.is_verified

        return data

class RegisterView(APIView):
  def post(self, request):
    try:
      data = request.data
      serializer = RegisterSerializer(data = data)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        send_otp_email(serializer.data['email'])
        return Response(serializer.data, status = status.HTTP_201_CREATED)
      else:
            print(serializer.errors)
            if 'password' in serializer.errors:
                error_detail = serializer.errors['password'][0]
                return Response({'message': 'invalid password', 'detail':error_detail.string},
                                    status=status.HTTP_400_BAD_REQUEST)
            if 'email' in serializer.errors:
                error_detail = serializer.errors['email'][0]
                return Response({'message':'invalid email', 'detail': error_detail.string}, status = status.HTTP_400_BAD_REQUEST)
               
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError as e:
        print(e)
        return Response({'message':'integrity error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except DatabaseError as e:
        print(e)
        return Response({'message':'database error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
      print(repr(e))
      return Response({'message':'server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      

class VerifyOTPView(APIView):
  def post(self, request):
    data = request.data
    serializer = VerifyOTPSerializer(data = data)
    if serializer.is_valid():
      email = serializer.data['email']
      otp = serializer.data['otp']

      user = User.objects.filter(email = email)
      if not user:
        return Response({
            
            'message' : 'email not found',
            'detail' : {}
          }, status = status.HTTP_400_BAD_REQUEST)

      if user.first().otp != otp:
        return Response({   
            'message' : 'wrong otp',
            'detail' : {}
          }, status = status.HTTP_400_BAD_REQUEST)

      user = user.first()

      user.is_verified = True
      user.save()
      return Response({
          'message' : 'otp verification successful',
          'detail' : serializer.data
        }, status=status.HTTP_200_OK)
    return Response({
           
            'message' : 'invalid data',
            'detail' : {}
          },status = status.HTTP_500_INTERNAL_SERVER_ERROR) 


@api_view(['GET'])
def is_unique_email(request,email):
    
    user = User.objects.filter(email=email)
    if user:
       return Response({'unique': False})
    return Response({'unique':True})
    

@api_view(['PATCH'])
def suspend_user(request):
    user_id = request.data['user_id']
    try:
        user = User.objects.get(id=user_id)
        if user:
           user.is_active = False
           user.save()
           return Response({'message':'user suspended'}, status=status.HTTP_200_OK)
    
    except:
       return Response({'message':'errir'}, status=status.HTTP_400_BAD_REQUEST)
  
