from django.urls import path
from .views import AddExpenseView, BalanceView

urlpatterns = [
    path('add_expense/', AddExpenseView.as_view(), name='add_expense'),
    path('balances/<int:user_id>/', BalanceView.as_view(), name='balances'),
]
