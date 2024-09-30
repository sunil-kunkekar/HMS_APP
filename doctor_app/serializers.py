# doctor_app/serializers.py

from rest_framework import serializers
from .models import DoctorFileUpload

# doctor_app/serializers.py

from rest_framework import serializers
from .models import DoctorFileUpload

class DoctorFileUploadSerializer(serializers.ModelSerializer):
    # Custom field for providing the file size in a human-readable format
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = DoctorFileUpload
        fields = ['id', 'doctor', 'file', 'description', 'uploaded_at', 'file_size']
        read_only_fields = ['doctor', 'uploaded_at', 'file_size']  # Make doctor, uploaded_at, and file_size read-only

    def get_file_size(self, obj):
        """Calculate the file size in MB."""
        size = obj.file.size  # Get the size in bytes
        return round(size / (1024 * 1024), 2)  # Convert to MB and round to 2 decimal places

    def validate_file(self, value):
        """Validate the uploaded file for size and type."""
        # Example: Limit the file size to 5 MB
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size should not exceed 5 MB.")
        
        # Example: Allow only specific file types
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Unsupported file type. Allowed types: PDF, JPEG, PNG.")

        return value

    def create(self, validated_data):
        """Override the create method to customize the saving behavior."""
        # The 'doctor' field is set to the authenticated user in the view, so it's not in validated_data.
        return DoctorFileUpload.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Override the update method if you want to customize the update behavior."""
        instance.file = validated_data.get('file', instance.file)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

