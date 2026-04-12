#!/bin/bash

# Michael Todd Beauty ERP - Installation Script
# This script sets up the complete Django ERP system

set -e

echo "=========================================="
echo "Michael Todd Beauty ERP Setup"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create migrations
echo ""
echo "Creating database migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations items
python manage.py makemigrations vendors
python manage.py makemigrations procurement
python manage.py makemigrations receiving
python manage.py makemigrations inventory
python manage.py makemigrations invoicing

# Apply migrations
echo ""
echo "Applying migrations..."
python manage.py migrate

# Create directories
echo ""
echo "Creating media and static directories..."
mkdir -p media/ppo_pdfs
mkdir -p media/proforma_invoices
mkdir -p media/ap_invoices
mkdir -p staticfiles

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
echo ""
echo "Creating superuser..."
python manage.py shell << EOF
from accounts.models import User
import os

# Check if admin already exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@michaeltodd.com',
        password='admin123',
        first_name='System',
        last_name='Administrator',
        role='admin'
    )
    print("✓ Superuser 'admin' created successfully!")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Email: admin@michaeltodd.com")
else:
    print("✓ Admin user already exists")
EOF

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "2. Access the system:"
echo "   Dashboard: http://localhost:8000/"
echo "   Admin: http://localhost:8000/admin/"
echo ""
echo "3. Login with:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "=========================================="
