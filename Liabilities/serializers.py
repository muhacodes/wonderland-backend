from rest_framework import serializers
from .models import LiabilityUser, Liability

class LiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Liability
        fields = ['id', 'date', 'amount', 'user']

class LiabilityUserSerializer(serializers.ModelSerializer):
    total_amount = serializers.ReadOnlyField(source='total_amount')
    liabilities = LiabilitySerializer(many=True, read_only=True)

    class Meta:
        model = LiabilityUser
        fields = ['id', 'name', 'contact', 'total_amount', 'liabilities']