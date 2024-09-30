# doctor_app/urls.py

from django.urls import path
from .views import FileUploadView, FileListView

urlpatterns = [
    path('doctors/upload/', FileUploadView.as_view(), name='file_upload'),
    path('doctors/uploads/', FileListView.as_view(), name='file_list'),
]
