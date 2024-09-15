from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('climate_app.urls')),  # Include your existing app's URLs (optional if applicable)
    path('', include('grid_model.urls')),
    path('', include('ai_mcq.urls')),
]