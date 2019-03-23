from django.db import models

# Create your models here.
class Order(models.Model):
    customer_id = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    created_at = models.DateTimeField('date')

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)