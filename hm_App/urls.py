from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router and register your viewsets with it.
router = DefaultRouter()

# Since we are not using viewsets, we will manually add the paths
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),  # Add this line
]
