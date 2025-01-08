from rest_framework import serializers
from .models import Sale, Expense

class SaleSerializer(serializers.ModelSerializer):
    cafe_profit = serializers.ReadOnlyField()  # Expose the property as a read-only field
    total_profit = serializers.ReadOnlyField()  # Expose the property as a read-only field

    class Meta:
        model = Sale
        fields = '__all__'  # Include all fields from the model
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.ladies_night:
            representation['Event'] = 'Ladies Night'
        elif instance.Event:
            representation['Event'] = instance.Event
        else:
            representation['Event'] = 'N/A'
        return representation


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'  # Include all fields from the model