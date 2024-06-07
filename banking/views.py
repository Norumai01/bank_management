from django.shortcuts import render, redirect
from .models import Customer, Account, Transaction
from .forms import CustomerForm, AccountForm, TransactionForm, BalanceForm

def index(request):
    return render(request, 'banking/index.html')

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomerForm()
    return render(request, 'banking/create_customer.html', {'form': form})

def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AccountForm()
    return render(request, 'banking/create_account.html', {'form': form})

def perform_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            account = transaction.account
            if transaction.transaction_type == 'DEPOSIT':
                account.balance += transaction.amount
            elif transaction.transaction_type == 'WITHDRAWAL':
                if account.balance >= transaction.amount:
                    account.balance -= transaction.amount
                else:
                    form.add_error(None, 'Insufficient funds')
                    return render(request, 'banking/perform_transaction.html', {'form': form})
            account.save()
            transaction.save()
            return redirect('index')
    else:
        form = TransactionForm()
    return render(request, 'banking/perform_transaction.html', {'form': form})

def view_balance(request):
    balance = None
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            balance = account.balance
    else:
        form = BalanceForm()
    return render(request, 'banking/view_balance.html', {'form': form, 'balance': balance})