from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get/', views.get_countdown, name='get_countdown'),
    path('set/', views.set_countdown, name='set_countdown'),
]
