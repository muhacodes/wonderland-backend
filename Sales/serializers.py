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

        if instance.Event:
            representation['Event'] = instance.Event
        else:
            representation['Event'] = 'N/A'
        return representation


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'  # Include all fields from the model

    

from rest_framework import serializers
from .models import InventoryItem, Category, SubCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested category details
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )  # Allow setting category by ID

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category', 'category_id']


class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested category details
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )  # Allow setting category by ID

    subcategory = SubCategorySerializer(read_only=True)  # Nested subcategory details
    subcategory_id = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all(), source="subcategory", write_only=True
    )  # Allow setting subcategory by ID

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'category', 'category_id', 'subcategory', 'subcategory_id', 
            'supplier', 'unit_of_measure', 'quantity_on_hand', 'minimum_stock_level', 
            'maximum_stock_level', 'cost_per_unit', 'total_cost', 'expiration_date', 
            'storage_location', 'restock_needed', 'last_updated', 'notes'
        ]
