# banking/urls.py
from django.urls import path
from .views import index, create_customer, create_account, perform_transaction, view_balance, register, user_login, customer_dashboard

urlpatterns = [
    path('', index, name='index'),
    path('create-account/', create_account, name='create_account'),
    path('perform-transaction/', perform_transaction, name='perform_transaction'),
    path('view-balance/', view_balance, name='view_balance'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('dashboard/', customer_dashboard, name='customer_dashboard'),
]
