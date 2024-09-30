from django.contrib import admin
admin.site.site_header = "Ecommerce Admin"
admin.site.site_title  = "Ecommerce TOOL"
admin.site.index_title = "Ecommerce"
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView

# Create a router and register your viewsets with it.
router = DefaultRouter()

# Since we are not using viewsets, we will manually add the paths
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
