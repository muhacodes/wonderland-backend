from django.contrib import admin
from .models import Sale, Expense, InventoryItem, Category, SubCategory

# Register your models here.


admin.site.register(Sale)
admin.site.register(Expense)
admin.site.register(Category)
admin.site.register(InventoryItem)
admin.site.register(SubCategory)
