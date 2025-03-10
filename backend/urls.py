from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('countdown/', include('countdown.urls')),
]