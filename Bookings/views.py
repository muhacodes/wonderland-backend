from django.shortcuts import render
from .models import Booking
from .serializer import BookingSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()  # Retrieve all Sale objects
    serializer_class = BookingSerializer  # Use the SaleSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response_data = {"id": instance.id}  # Prepare the ID for the response
        self.perform_destroy(instance)
        return Response(response_data, status=status.HTTP_200_OK)