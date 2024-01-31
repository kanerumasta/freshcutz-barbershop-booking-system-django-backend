
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)  
        
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        token['is_active'] = user.is_active
        token['is_verified'] = user.is_verified
        return token
    
    def validate(self, attrs):
        
        try:
           email = attrs.get("email")
           user = User.objects.get(email=email)
        except:
           raise serializers.ValidationError("Email does not exists")
        # Check if the user is active
        if not user.is_active:
            raise serializers.ValidationError("User account is not active")
        if not user.is_verified:
            raise serializers.ValidationError("Account not verified")
        password = attrs.get("password")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        return data
    



class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="This email address is already in use.",
        )
    ],
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)
  class Meta:
    model = User
    fields = ('email','password','password2','first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs

  def create(self, validated_data):
    user = User.objects.create(
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class VerifyOTPSerializer(serializers.Serializer):
  email = serializers.EmailField()
  otp = serializers.CharField(max_length = 4)
