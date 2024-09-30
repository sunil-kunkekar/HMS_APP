
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Custom_User
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# class RegisterView(generics.CreateAPIView):
#     queryset = Custom_User.objects.all()
#     serializer_class = UserSerializer

class UserRegistrationView_main(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the new user
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = Custom_User.objects.all()  # Fetch all users
        serializer = UserSerializer(users, many=True)  # Serialize user data
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework_simplejwt.tokens import RefreshToken
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = Custom_User.objects.get(email=email)
                if user.check_password(password):
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        'msg': 'Login successful',
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except Custom_User.DoesNotExist:
                return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework import status, generics, permissions
class UserProfileView(generics.RetrieveAPIView):
    queryset = Custom_User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Adjust permissions as needed

    def get_object(self):
        # Return the user instance for the currently authenticated user
        return self.request.user