from django.db import models

# Create your models here.

class Sale(models.Model):
    date                        = models.DateField()
    Event                       = models.CharField(null=True, blank=True, max_length=500)
    event_amount                = models.DecimalField(decimal_places=2, max_digits=13)
    ladies_night                = models.BooleanField(default=False)
    cafe_sales                  = models.DecimalField(max_digits=13, decimal_places=2)
    arcade_sales                = models.DecimalField(max_digits=13, decimal_places=2)
    cafe_expenses               = models.DecimalField(max_digits=13, decimal_places=2)
    other_expenses              = models.DecimalField(max_digits=13, decimal_places=2)

    @property
    def cafe_profit(self):
        """
        Calculate the total liability amount for this user.
        """
        if self.ladies_night:
            return None
        return self.cafe_sales + self.event_amount - self.cafe_expenses or 0
        
        # return self.liabilities.aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
    
    @property
    def total_profit(self):
        """
        Calculate the total liability amount for this user.
        """
        if self.ladies_night:
            return self.arcade_sales - self.other_expenses
        return self.cafe_profit + self.arcade_sales - self.other_expenses
    
    def get_total_profit(self):
        """
        Method to access total_profit for database queries.
        """
        if self.ladies_night:
            return F('arcade_sales') - F('other_expenses') 
        else:
            return (F('cafe_sales') - F('cafe_expenses')) + F('arcade_sales') - F('other_expenses')


class Expense(models.Model):
    date                        = models.DateField()
    name                        = models.DecimalField(max_digits=13, decimal_places=2)
    amount                      = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.amount}"
    