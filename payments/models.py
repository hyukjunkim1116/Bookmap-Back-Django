from django.db import models
from users.models import User
from django.utils import timezone


class Payment(models.Model):
    class Meta:
        db_table = "Payment"

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    amount = models.CharField(
        max_length=40,
        default="",
        null=False,
    )
    imp = models.CharField(
        max_length=5000,
        default="",
        null=False,
    )
    merchant = models.CharField(
        max_length=5000,
        default="",
        null=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.buyer)
