from django.db import models
from django.conf import settings
from menu.models import MenuItem

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    session_key = models.CharField(max_length=40, blank=True)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'session_key', 'item')

    def line_total(self):
        return self.quantity * self.item.price

    def __str__(self):
        who = self.user or self.session_key
        return f'{who} – {self.item.name} × {self.quantity}'
