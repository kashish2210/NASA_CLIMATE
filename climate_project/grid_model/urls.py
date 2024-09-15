from django.urls import path
from . import views

urlpatterns = [
   path('grid/', views.grid_page, name='grid_page'),
   path('run/', views.run_testpy, name='run_testpy'),
   path('index/', views.index, name='index'),
]