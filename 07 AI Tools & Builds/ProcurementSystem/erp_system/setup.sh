#!/bin/bash
# ============================================================
# Michael Todd Beauty - ERP Procurement System Setup
# ============================================================
# Run this script from the erp_system/ directory:
#   cd ProcurementSystem/erp_system
#   bash setup.sh
# ============================================================

set -e

echo ""
echo "=================================================="
echo "  Michael Todd Beauty - ERP System Setup"
echo "=================================================="
echo ""

# Check Python version
echo "[0/7] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=pip3
elif command -v python &> /dev/null; then
    PYTHON=python
    PIP=pip
else
    echo "ERROR: Python not found. Please install Python 3.9+."
    exit 1
fi
echo "      Using: $($PYTHON --version)"

# Step 1: Create virtual environment (recommended)
echo ""
echo "[1/7] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
    echo "      Virtual environment created."
else
    echo "      Virtual environment already exists."
fi

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
fi
echo "      Activated."

# Step 2: Install Python dependencies
echo ""
echo "[2/7] Installing Python dependencies..."
pip install -r requirements.txt
echo "      Done."

# Step 3: Run database migrations
echo ""
echo "[3/7] Creating database tables..."
python manage.py makemigrations accounts core items vendors procurement receiving inventory invoicing
python manage.py migrate
echo "      Done."

# Step 4: Create directories
echo ""
echo "[4/7] Creating media directories..."
mkdir -p media/ppo_pdfs media/ppo_attachments media/proforma_invoices media/ap_invoices
mkdir -p static/css static/js staticfiles
echo "      Done."

# Step 5: Import data from Excel
echo ""
echo "[5/7] Importing data from Excel (603 items, vendors, addresses)..."
python data_migration/migrate_excel.py
echo "      Done."

# Step 6: Create users
echo ""
echo "[6/7] Creating users..."
python manage.py shell -c "
from accounts.models import User
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'supplychain@michaeltoddbeauty.com', 'admin123')
    u.first_name = 'Tommy'
    u.last_name = 'Sapia'
    u.role = 'supply_chain_manager'
    u.department = 'Supply Chain'
    u.save()
    print('  Supply Chain Manager created: admin / admin123')
else:
    print('  Admin user already exists.')
if not User.objects.filter(username='ceo').exists():
    u = User.objects.create_user('ceo', 'ceo@michaeltoddbeauty.com', 'ceo123')
    u.first_name = 'CEO'
    u.last_name = 'Michael Todd'
    u.role = 'admin'
    u.department = 'Executive'
    u.is_staff = True
    u.save()
    print('  CEO user created: ceo / ceo123')
else:
    print('  CEO user already exists.')
"
echo "      Done."

# Step 7: Collect static files
echo ""
echo "[7/7] Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true
echo "      Done."

echo ""
echo "=================================================="
echo "  Setup Complete!"
echo "=================================================="
echo ""
echo "  To start the server, run:"
echo ""
echo "    source venv/bin/activate"
echo "    python manage.py runserver"
echo ""
echo "  Then open: http://localhost:8000"
echo ""
echo "  Login credentials:"
echo "    Supply Chain Manager:  admin / admin123"
echo "    CEO (for approvals):   ceo / ceo123"
echo ""
echo "  Django Admin: http://localhost:8000/admin/"
echo ""
echo "=================================================="
