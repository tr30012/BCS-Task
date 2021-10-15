from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=64)
    datetime = models.DateTimeField(auto_now=True)
    value = models.DecimalField(max_digits=16, decimal_places=8)
    jsontext = models.TextField()
    description = models.TextField()

