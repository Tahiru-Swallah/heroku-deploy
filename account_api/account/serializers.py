from rest_framework import serializers
from .models import CustomUser, Profile
from django.contrib.auth.hashers import make_password

class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'password'
        ]

    def validate(self, attrs):
        # Ensure username is unique
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({'username': 'This username is already taken.'})

        # Ensure email is unique
        if attrs.get('email') and CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': 'This email is already taken.'})

        # Ensure phone number is unique
        if attrs.get('phone_number') and CustomUser.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({'phone_number': 'This phone number is already taken.'})

        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove password from validated_data
        user = CustomUser(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user

        Profile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not (email or phone_number):
            raise serializers.ValidationError('Email or Phone number required')

        user = None

        if email:
            user = CustomUser.objects.filter(email=email).first()
        else:
            user = CustomUser.objects.filter(phone_number=phone_number).first()
        
        if not user:
            raise serializers.ValidationError("Invalid Credentials")

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid Password')

        data['user'] = user

        return data        
    
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Invalid current password")
        return value

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.password = make_password(new_password)
        user.save()