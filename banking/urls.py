# banking/urls.py
from django.urls import path
from .views import index, create_customer, create_account, perform_transaction, view_balance

urlpatterns = [
    path('', index, name='index'),
    path('create-customer/', create_customer, name='create_customer'),
    path('create-account/', create_account, name='create_account'),
    path('perform-transaction/', perform_transaction, name='perform_transaction'),
    path('view-balance/', view_balance, name='view_balance'),
]
