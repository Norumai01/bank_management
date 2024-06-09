from django import forms
from django.contrib.auth.models import User
from .models import Customer, Account, Transaction

class UserRegisterationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone']

class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CustomerForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['customer'].queryset = Account.objects.filter(customer=user.customer) # Bug: Drop-down menu shows name and account types dupes.
    
    class Meta:
        model = Account
        fields = ['customer', 'account_type', 'balance']

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        account_type = cleaned_data.get('account_type')

        if Account.objects.filter(customer=customer, account_type=account_type).exists():
            raise forms.ValidationError(f'The customer already has a {account_type} account.')
        return cleaned_data

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            self.fields['account'].queryset = Account.objects.filter(customer=user.customer)
    
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_type', 'amount']

class BalanceForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Select Account")