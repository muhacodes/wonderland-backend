from rest_framework import serializers
from .models import Booking



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'  # Include all fields from the model