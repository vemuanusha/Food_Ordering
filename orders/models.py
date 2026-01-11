from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user        = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    placed_at   = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items',
                                 on_delete=models.CASCADE)
    item     = models.ForeignKey('menu.MenuItem', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} × {self.item.name}"
