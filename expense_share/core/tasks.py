import csv
import boto3
from celery import shared_task
from django.conf import settings
from .models import User, Balance

@shared_task
def export_balances_to_s3():
    s3 = boto3.client('s3')
    users = User.objects.all()
    filename = '/tmp/balances.csv'
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User ID', 'Owed To User ID', 'Amount'])
        for user in users:
            balances_owed = Balance.objects.filter(from_user=user)
            for balance in balances_owed:
                writer.writerow([user.id, balance.to_user.id, balance.amount])
    s3.upload_file(filename, 'your-bucket-name', 'balances.csv')
