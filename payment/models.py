from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'PRICE: {self.price} ITEM: {self.name}'
