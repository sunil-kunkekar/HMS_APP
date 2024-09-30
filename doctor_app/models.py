from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class DoctorFileUpload(models.Model):
    doctor      = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the doctor
    file        = models.FileField(upload_to='doctor_uploads/')  # Directory where files will be uploaded
    description = models.CharField(max_length=255, blank=True, null=True)  # Description of the file
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Date and time of upload

    def __str__(self):
        return f"{self.doctor.name} - {self.file.name}"
