from django.urls import path
from . import views  # Import from the climate_app # Import the views module from the current app

urlpatterns = [
    path('', views.home, name='home'),
    path('anim/', views.anim, name='anim'),
     path('water/', views.water, name='water'),
     path('solar/', views.solar, name='solar'),
]