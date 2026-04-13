# Michael Todd Beauty ERP - Procurement System Setup

## Project Structure

This is a complete Django-based ERP system for managing the procurement process at Michael Todd Beauty.

## Quick Start

### 1. Create a Virtual Environment

```bash
cd /sessions/hopeful-ecstatic-mendel/mnt/ProcurementSystem/erp_system
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a Superuser

```bash
python manage.py createsuperuser
```

Or use the Django shell to create a user with our User model:

```bash
python manage.py shell
>>> from accounts.models import User
>>> User.objects.create_superuser('admin', 'admin@michaeltodd.com', 'admin123', role='admin')
>>> exit()
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the system.

### Default Admin Credentials

- Username: `admin`
- Password: `admin123`
- Email: `admin@michaeltodd.com`

## Project Layout

### Apps

- **accounts**: User authentication and role management
- **items**: Item master data management
- **vendors**: Vendor management (Vendors, Bill-To, Ship-To addresses)
- **procurement**: Purchase Requisitions, Purchase Orders (PPO), Proforma Invoices
- **receiving**: Goods Receipt PO (GRPO) and receiving process
- **inventory**: Warehouse management, stock levels, and stock movements
- **invoicing**: AP Invoice management and 3-way matching

### Key Models

1. **User** (Custom Auth User)
   - Roles: Admin, Supply Chain Manager, Buyer, Warehouse Staff, Finance/AP, Viewer
   - Permissions based on role

2. **Item**
   - Complete item master with carton calculations
   - ABC classification support
   - Master carton volume and CBM calculations

3. **Vendor**
   - Contact information
   - Payment terms and lead time
   - Wire/Bank information

4. **PlannedPurchaseOrder (PPO)**
   - Core procurement document
   - Multiple transport modes (Container, Air, LCL, Truck)
   - Incoterms support
   - Line items with auto-calculated cartons and CBM
   - Deposit tracking

5. **GoodsReceiptPO (GRPO)**
   - Receiving process
   - Quantity variance tracking
   - Batch number and expiry date support

6. **APInvoice**
   - 3-way matching capability (PO vs GRPO vs Invoice)
   - Payment tracking

## Features

### Procurement Module
- Create and manage Purchase Requisitions (PR)
- Generate Planned Purchase Orders (PPO) from PRs
- Support for multiple vendors, ship-to addresses, incoterms
- Automatic carton and CBM calculations
- Proforma Invoice (PI) management

### Receiving Module
- Create Goods Receipt POs (GRPO)
- Track received quantities vs expected quantities
- Damage tracking
- Batch and expiry date tracking

### Inventory Module
- Warehouse management
- Stock level tracking by warehouse
- Stock movement logging (In, Out, Adjustment, Transfer)

### Invoicing Module
- AP Invoice creation and tracking
- 3-way matching (PO vs GRPO vs Invoice) with tolerance
- Payment tracking

## Admin Interface

Access the Django admin at `/admin/` using superuser credentials.

All models are registered in Django Admin for easy management.

## Customization

### Adding Users
Users can be added through:
1. Django Admin (`/admin/`)
2. Create a management command (optional)

### Modifying Role Permissions
Edit the `can_*()` methods in `accounts/models.py` User class to customize permissions.

### Extending Models
All apps are fully extensible. Add fields to models in each app's `models.py` file, then:
```bash
python manage.py makemigrations <app_name>
python manage.py migrate
```

## Database

Currently configured to use SQLite (`db.sqlite3`). To switch to PostgreSQL:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'erp_procurement',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Run migrations as above

## URLs

- `/` - Dashboard
- `/login/` - Login page
- `/logout/` - Logout
- `/items/` - Items list
- `/vendors/` - Vendors list
- `/procurement/ppos/` - Purchase Orders
- `/procurement/requisitions/` - Purchase Requisitions
- `/procurement/proforma-invoices/` - Proforma Invoices
- `/receiving/` - Goods Receipts
- `/inventory/warehouses/` - Warehouses
- `/inventory/stock-levels/` - Stock Levels
- `/invoicing/` - AP Invoices
- `/admin/` - Django Admin

## Support for Tommy (Supply Chain Manager)

This system replaces the Excel-based PPO system with:

1. **Automated Calculations**: Cartons and CBM automatically calculated based on item master
2. **Vendor Management**: Centralized vendor database with payment terms and lead times
3. **Order Tracking**: Full order lifecycle from PR → PPO → GRPO → Invoice
4. **3-Way Matching**: Automatic matching of Purchase Orders, Goods Receipts, and Invoices
5. **User Roles**: Different access levels for different departments
6. **Audit Trail**: All changes tracked with timestamps and user information

## License

Internal use only - Michael Todd Beauty.
