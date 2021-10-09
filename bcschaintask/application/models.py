from django.db import models


def create_hex64():
    from random import randint
    return ''.join([str(randint(0, 9)) for i in range(64)])


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=64)
    datetime = models.DateTimeField(auto_now=True)
    value = models.DecimalField(max_digits=16, decimal_places=8)
    description = models.TextField()
