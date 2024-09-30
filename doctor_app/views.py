from django.shortcuts import render

# Create your views here.
# doctor_app/views.py

from rest_framework import generics, permissions
from .models import DoctorFileUpload
from .serializers import DoctorFileUploadSerializer

class FileUploadView(generics.CreateAPIView):
    queryset = DoctorFileUpload.objects.all()
    serializer_class = DoctorFileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Set the doctor field to the currently authenticated user
        serializer.save(doctor=self.request.user)

class FileListView(generics.ListAPIView):
    queryset = DoctorFileUpload.objects.all()
    serializer_class = DoctorFileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return files uploaded by the currently authenticated doctor
        return self.queryset.filter(doctor=self.request.user)
