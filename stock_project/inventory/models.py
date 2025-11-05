from django.db import models

# Create your models here.
class stockItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)  # 👈 Added line
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category =models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
