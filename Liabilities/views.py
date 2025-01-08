from rest_framework import viewsets
from .models import LiabilityUser, Liability
from .serializers import LiabilitySerializer, LiabilityUserSerializer

class LiabilityViewSet(viewsets.ModelViewSet):
    queryset = Liability.objects.all()
    serializer_class = LiabilitySerializer

class LiabilityUserViewSet(viewsets.ModelViewSet):
    queryset = LiabilityUser.objects.all()
    serializer_class = LiabilityUserSerializer