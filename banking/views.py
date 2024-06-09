from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerForm, AccountForm, TransactionForm, BalanceForm, UserRegisterationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Account
from django.contrib.auth.views import LogoutView
from django.db import IntegrityError

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('customer_dashboard')
    else:
        return redirect('login')

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            return create_user_and_customer(request, user_form, customer_form)
    else:
        user_form = UserRegisterationForm()
        customer_form = CustomerForm()
    return render(request, 'banking/register.html', {'user_form': user_form, 'customer_form': customer_form})

def create_user_and_customer(request, user_form, customer_form):
    try:
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        new_customer = customer_form.save(commit=False)
        new_customer.user = new_user
        new_customer.save()
        return redirect('login')
    except IntegrityError:
        user_form.add_error(None, 'A user with that email or phone number already exists.')
        return render(request, 'banking/register.html', {'user_form': user_form, 'customer_form': customer_form})

@login_required
def customer_dashboard(request):
    customer = request.user.customer
    accounts = Account.objects.filter(customer=customer)
    return render(request, 'banking/dashboard.html', {'customer': customer, 'accounts': accounts})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    return redirect('customer_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'banking/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'banking/admin_dashboard.html')

@login_required
def logout_view(request):
    return render(request, 'banking/logout.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CustomerForm()
    return render(request, 'banking/create_customer.html', {'form': form})

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AccountForm(user=request.user)
    return render(request, 'banking/create_account.html', {'form': form})

@login_required
def perform_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
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
        form = TransactionForm(user=request.user)
    return render(request, 'banking/perform_transaction.html', {'form': form})

@login_required
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