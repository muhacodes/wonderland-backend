from django.db import models

# Create your models here.

class Sale(models.Model):
    date                        = models.DateField()
    Event                       = models.CharField(null=True, blank=True, max_length=500)
    event_amount                = models.DecimalField(decimal_places=2, default=0, max_digits=13)
    cafe_sales                  = models.DecimalField(max_digits=13, decimal_places=2)
    arcade_sales                = models.DecimalField(max_digits=13, decimal_places=2)
    cafe_expenses               = models.DecimalField(max_digits=13, decimal_places=2)
    other_expenses              = models.DecimalField(max_digits=13, decimal_places=2)

    @property
    def cafe_profit(self):
        """
        Calculate the total liability amount for this user.
        """
        if self.event_amount:
            return self.cafe_sales + self.event_amount  - self.cafe_expenses
        return self.cafe_sales + self.event_amount - self.cafe_expenses or 0
        
        # return self.liabilities.aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    
    @property
    def total_profit(self):
        """
        Calculate the total liability amount for this user.
        """
        return self.cafe_profit + self.arcade_sales - self.other_expenses
    
    def get_total_profit(self):
        """
        Method to access total_profit for database queries.
        """
        
        return (F('cafe_sales') - F('cafe_expenses')) + F('arcade_sales') - F('other_expenses')
    
    # class Meta:
    #     ordering = ['-date']  # Order by 'date' descending by default


class Expense(models.Model):
    date                        = models.DateField()
    name                        = models.DecimalField(max_digits=13, decimal_places=2)
    amount                      = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.amount}"
    


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the category

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)  # Name of the subcategory
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to category

    class Meta:
        unique_together = ('name', 'category')  # Ensure uniqueness within a category

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class InventoryItem(models.Model):
    name = models.CharField(max_length=255)  # Item Name
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")  # Link to category
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="items")  # Link to subcategory
    supplier = models.CharField(max_length=255)  # Supplier
    unit_of_measure = models.CharField(max_length=50)  # Unit of Measure (e.g., kg, liters)
    quantity_on_hand = models.FloatField()  # Quantity available
    minimum_stock_level = models.FloatField()  # Minimum stock level
    maximum_stock_level = models.FloatField()  # Maximum stock level
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Cost per unit
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)  # Total cost
    expiration_date = models.DateField(null=True, blank=True)  # Expiration date
    storage_location = models.CharField(max_length=255)  # Storage location
    restock_needed = models.BooleanField(default=False)  # Indicates if restock is needed
    last_updated = models.DateTimeField(auto_now=True)  # Timestamp for the last update
    notes = models.TextField(blank=True)  # Notes for the item

    def __str__(self):
        return self.name