from django.db import models


# Create your models here.
class Discount(models.Model):
    stripe_id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    percent_off = models.PositiveIntegerField(null=True, blank=True)
    amount_off = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"DISCOUNT ID: {self.stripe_id} NAME: {self.name} ACTIVE: {self.active}"


class Tax(models.Model):
    tax_rate_id = models.CharField(primary_key=True, max_length=50)
    type = models.CharField(max_length=25)
    region = models.CharField(max_length=25)
    rate = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"TYPE: {self.type} RATE: {self.rate} REGION: {self.region} ACTIVE: {self.active}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, null=True)

    def total_price(self):
        return sum(item.total_price() for item in self.order_items.all())

    def __str__(self):
        return f"ORDER ID: {self.id} DISCOUNT: [{self.discount}] TAX: {self.tax}"


class Item(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        default='usd',
        choices=[
            ('usd', 'USD'),
            ('eur', 'EUR'),
        ]
    )

    def __str__(self):
        return f'ID: {self.id} PRICE: {self.price} ITEM: {self.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"ORDER ID: {self.order.id} ITEM: {self.item.name}"
