from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

class Expense(models.Model):
    EQUAL = 'EQUAL'
    EXACT = 'EXACT'
    PERCENT = 'PERCENT'
    SPLIT_CHOICES = [
        (EQUAL, 'Equal'),
        (EXACT, 'Exact'),
        (PERCENT, 'Percent'),
    ]
    payer = models.ForeignKey(User, related_name='paid_expenses', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

class Balance(models.Model):
    from_user = models.ForeignKey(User, related_name='balances_owed', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='balances_owing', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('from_user', 'to_user')
