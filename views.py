from django.db import models
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import path
from django.http import JsonResponse
from rest_framework import status
import django

# Initialize Django settings (only necessary for standalone scripts)
django.setup()

# Step 1: Define the City model
class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Step 2: Create the CitySerializer
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

# Step 3: Create the POST API that saves city data and returns the serialized data with the count
@api_view(['POST'])
def add_cities(request):
    # Step 4: Get data from the request (Expecting data in the format: {"cities": ["City1", "City2", ...]})
    data = request.data
    city_names = data.get('cities', [])
    
    # Step 5: Save cities to the database
    saved_cities = []
    for name in city_names:
        city, created = City.objects.get_or_create(name=name)
        if created:  # Add only newly created cities
            saved_cities.append(city)

    # Step 6: Serialize the saved cities
    serializer = CitySerializer(saved_cities, many=True)
    
    # Step 7: Prepare response with serialized data and count of saved cities
    response_data = {
        'saved_count': len(saved_cities),
        'cities': serializer.data
    }

    # Return the response with a 201 created status
    return JsonResponse(response_data, status=status.HTTP_201_CREATED)

# Step 8: URL Configuration
urlpatterns = [
    path('add-cities/', add_cities, name='add_cities'),
]

