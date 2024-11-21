from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('auth/', include('Authentication.urls')),
    path('mgnt/',include('Management.urls')),
]
