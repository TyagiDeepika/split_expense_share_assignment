from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Expense, Balance
from .serializers import ExpenseSerializer

class AddExpenseView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = serializer.save()
            participants = request.data['participants']
            split_type = request.data['split_type']
            amount = expense.amount

            if split_type == Expense.EQUAL:
                share = amount / len(participants)
                for user_id in participants:
                    user = get_object_or_404(User, id=user_id)
                    if user != expense.payer:
                        self.update_balance(expense.payer, user, share)
            elif split_type == Expense.EXACT:
                exact_shares = request.data['exact_shares']
                if sum(exact_shares.values()) != amount:
                    return Response({"error": "Exact shares do not sum up to total amount"}, status=status.HTTP_400_BAD_REQUEST)
                for user_id, share in exact_shares.items():
                    user = get_object_or_404(User, id=user_id)
                    if user != expense.payer:
                        self.update_balance(expense.payer, user, share)
            elif split_type == Expense.PERCENT:
                percent_shares = request.data['percent_shares']
                if sum(percent_shares.values()) != 100:
                    return Response({"error": "Percent shares do not sum up to 100%"}, status=status.HTTP_400_BAD_REQUEST)
                for user_id, percent in percent_shares.items():
                    user = get_object_or_404(User, id=user_id)
                    share = amount * (percent / 100)
                    if user != expense.payer:
                        self.update_balance(expense.payer, user, share)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_balance(self, payer, user, amount):
        balance, created = Balance.objects.get_or_create(from_user=user, to_user=payer)
        balance.amount = F('amount') + amount
        balance.save()

class BalanceView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        balances_owed = Balance.objects.filter(from_user=user)
        balances_owing = Balance.objects.filter(to_user=user)
        data = {
            "balances_owed": [{ "to": b.to_user.id, "amount": b.amount } for b in balances_owed],
            "balances_owing": [{ "from": b.from_user.id, "amount": b.amount } for b in balances_owing],
        }
        return Response(data)
