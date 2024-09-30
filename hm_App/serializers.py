

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

# accounts/serializers.py

from rest_framework import serializers
from .models import Custom_User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_User
        fields = ['id', 'email', 'name', 'tc', 'is_active']  


from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email')
        if Custom_User.objects.filter(email=email).exists():
            user = Custom_User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://localhost:5555/api/User/reset-password/{uid}/{token}'
            body = f'Click the following link to reset your password: {link}'
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email,
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError(_("You are not a registered user"))

class UserChangePasswordSerializer(serializers.Serializer):
    password         = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')

        if password != confirm_password:
            raise serializers.ValidationError(_("Password and Confirm Password don't match"))

        user.set_password(password)
        user.save()
        return attrs


from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserPasswordResetSerializer(serializers.Serializer):
    password         = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        try:
            password         = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uid              = self.context.get('uid')
            token            = self.context.get('token')

            if password != confirm_password:
                raise serializers.ValidationError(_("Password and Confirm Password don't match"))

            user_id = smart_str(urlsafe_base64_decode(uid))
            user    = Custom_User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(_('Token is not valid or has expired'))

            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError(_('Token is not valid or has expired'))
        
        
from rest_framework import serializers
from .models import Patient, MedicalRecord

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',               # Add patient ID for reference
            'user',             # Link to the user model
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'phone_number',
            'address',
            'created_at',
            'updated_at',
        ]

    def validate_email(self, value):
        """Check if the email is already registered."""
        if Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def create(self, validated_data):
        """Create a new Patient instance."""
        user_data = validated_data.pop('user')  # Extract user data if needed
        patient = Patient.objects.create(**validated_data)  # Create the patient instance
        return patient

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = [
            'id',               # Add record ID for reference
            'patient',
            'record_date',
            'diagnosis',
            'treatment',
            'prescription_file',
            'created_at',
            'updated_at',
        ]

    def validate_prescription_file(self, value):
        """Validate the uploaded prescription file."""
        if value:
            if not value.name.endswith('.pdf'):
                raise serializers.ValidationError("Prescription file must be a PDF.")
            if value.size > 5 * 1024 * 1024:  # Limit file size to 5 MB
                raise serializers.ValidationError("File size must be under 5MB.")
        return value

    def create(self, validated_data):
        """Create a new MedicalRecord instance."""
        medical_record = MedicalRecord.objects.create(**validated_data)
        return medical_record
