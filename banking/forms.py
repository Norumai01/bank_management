from django import forms
from .models import Customer, Account, Transaction

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['customer', 'account_type', 'balance']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_type', 'amount']

class BalanceForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Select Account")