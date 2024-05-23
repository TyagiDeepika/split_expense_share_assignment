from rest_framework import serializers
from .models import User, Expense, Balance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'payer', 'amount', 'description', 'split_type', 'date']
