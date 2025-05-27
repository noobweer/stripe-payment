from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'PRICE: {self.price} ITEM: {self.name}'


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.order_items.all())

    def __str__(self):
        return f"ORDER ID: {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.name}"
