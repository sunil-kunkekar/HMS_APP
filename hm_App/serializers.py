# accounts/serializers.py

from rest_framework import serializers
from .models import Custom_User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Custom_User
        fields = ['id', 'email', 'name', 'tc', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def create(self, validated_data):
        # Remove confirm_password field
        validated_data.pop('confirm_password')
        
        user = Custom_User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, attrs):
        # Validate password and confirm_password match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        return attrs
