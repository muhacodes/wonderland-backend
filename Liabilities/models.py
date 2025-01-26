from django.db import models
from Management.models import StaffProfile

class LiabilityUser(models.Model):
    name = models.CharField(max_length=500)
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def total_amount(self):
        """
        Calculate the total liability amount for this user.
        """
        return self.liabilities.aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0


class Liability(models.Model):
    date        = models.DateField()
    amount      = models.DecimalField(decimal_places=2, max_digits=13)
    user        = models.CharField(max_length=500, null=True, blank=True)
    # user = models.ForeignKey(LiabilityUser, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.user} {self.amount} on  {self.date}"