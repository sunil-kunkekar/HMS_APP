
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Custom_User
from .serializers import *

class RegisterView(generics.CreateAPIView):
    queryset = Custom_User.objects.all()
    serializer_class = UserSerializer

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             try:
#                 user = Custom_User.objects.get(email=email)
#                 if user.check_password(password):
#                     return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#             except Custom_User.DoesNotExist:
#                 return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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