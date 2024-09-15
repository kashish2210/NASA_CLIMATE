from django.db import models
class ClimateData(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    precipitation = models.FloatField()
    # Add other fields as needed

class Visualization(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # Add fields for storing visualization data (e.g., a JSON field)

