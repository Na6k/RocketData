from django.contrib.auth.models import User
import random
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fill the user table with test data about employees'

    def handle(self, *args, **options):
        users = []
        for _ in range(10):
            username = f"user_{random.randint(1, 10000)}"
            email = f"{username}@example.com"
            password = "123456"
            users.append(User(username=username, email=email, password=password, is_staff = False))
        User.objects.bulk_create(users)    

        
       
