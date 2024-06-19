from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Account(models.Model):
    ACCOUNT_TYPES_CHOICES = [
        ('SAVINGS', 'Savings'),
        ('CHECKING', 'Checking'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'account_type')
    
    def __str__(self):
        return f'{self.customer} - {self.account_type}'
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.account} - {self.transaction_type} - {self.amount}'