# banking/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import index, create_account, perform_transaction, view_balance, register, user_login, customer_dashboard, logout_view, create_customer, admin_dashboard

urlpatterns = [
    path('', index, name='index'),
    path('create-account/', create_account, name='create_account'),
    path('create-customer/', create_customer, name='create_customer'),
    path('perform-transaction/', perform_transaction, name='perform_transaction'),
    path('view-balance/', view_balance, name='view_balance'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout/confirm/', LogoutView.as_view(next_page='index'), name='logout_confirm'),
    path('dashboard/', customer_dashboard, name='customer_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]
