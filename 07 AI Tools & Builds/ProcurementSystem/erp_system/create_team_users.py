#!/usr/bin/env python
"""
Create team user accounts for Michael Todd Beauty ERP.
Run from the erp_system directory:
    python manage.py shell < create_team_users.py
"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')
django.setup()

from accounts.models import User

TEAM = [
    {
        'username': 'tom',
        'first_name': 'Tom',
        'last_name': 'Sapia',
        'email': 'tom@michaeltoddbeauty.com',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
        'password': 'MTB2024!',
    },
    {
        'username': 'augusto',
        'first_name': 'Augusto',
        'last_name': '',
        'email': 'augusto@michaeltoddbeauty.com',
        'role': 'supply_chain_manager',
        'is_staff': False,
        'is_superuser': False,
        'password': 'MTB2024!',
    },
    {
        'username': 'donna',
        'first_name': 'Donna',
        'last_name': '',
        'email': 'donna@michaeltoddbeauty.com',
        'role': 'supply_chain_manager',
        'is_staff': False,
        'is_superuser': False,
        'password': 'MTB2024!',
    },
]

for info in TEAM:
    user, created = User.objects.get_or_create(
        username=info['username'],
        defaults={
            'first_name': info['first_name'],
            'last_name': info['last_name'],
            'email': info['email'],
            'role': info['role'],
            'is_staff': info['is_staff'],
            'is_superuser': info['is_superuser'],
        }
    )
    if created:
        user.set_password(info['password'])
        user.save()
        print(f"  Created user: {info['username']} ({info['role']})")
    else:
        print(f"  User already exists: {info['username']}")

print("\nAll team accounts ready!")
print("Default password for new accounts: MTB2024!")
print("Please have each user change their password after first login.")
