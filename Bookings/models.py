from django.db import models

# Create your models here.


class Booking(models.Model):
    date                    = models.DateField()
    booking_type            = models.CharField(max_length=500)
    people                  = models.SmallIntegerField()
    videographer            = models.BooleanField(default=False)
    decoration              = models.BooleanField(default=True)
    price                   = models.DecimalField(max_digits=10, decimal_places=2)
    paid                    = models.BooleanField(default=False)