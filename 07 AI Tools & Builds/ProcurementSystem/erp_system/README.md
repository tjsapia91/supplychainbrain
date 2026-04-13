# Michael Todd Beauty ERP - Procurement System

A complete Django-based Enterprise Resource Planning (ERP) system designed specifically for Michael Todd Beauty's procurement operations. This system replaces the Excel-based PPO (Planned Purchase Order) system with a robust, scalable, and automated solution.

## Overview

Built for Tommy (Supply Chain Manager) and the procurement team, this system manages the complete procurement lifecycle:

```
Purchase Requisition → Planned Purchase Order → Proforma Invoice → Goods Receipt → AP Invoice Processing
```

## Key Features

### 1. Item Master Management
- Complete item database with unique item numbers
- ABC classification (High Volume, Low Volume, Phase-In, Phase-Out)
- Automatic carton and CBM (Cubic Meter) calculations
- Master carton volume tracking
- Multiple branches support (Michael Todd Beauty, Spa Sciences, NasaFresh MD)

### 2. Vendor Management
- Comprehensive vendor database
- Multiple addresses per vendor (Bill-To, Ship-To)
- Contact information and payment terms
- Lead time tracking
- Wire/bank transfer information
- Vendor rating system

### 3. Procurement Module
- **Purchase Requisitions (PR)**: Create and approve requisitions
- **Planned Purchase Orders (PPO)**: Main procurement document with:
  - Automatic PPO numbering (starting from 3149)
  - Multiple transport modes (Container, Air, LCL, Truck)
  - Incoterms support (DDP, FOB, CIF, EXW, CFR, DAP)
  - Port information (loading/discharge)
  - Deposit tracking and balance calculations
  - Auto-calculated line totals and carton counts
  - PDF generation capability
- **Proforma Invoices**: Upload and track vendor PIs

### 4. Receiving & Inventory
- **Goods Receipt PO (GRPO)**: Track incoming shipments
  - Quantity variance tracking
  - Damage reporting
  - Batch number and expiry date support
  - Auto-numbering (starting from 1001)
- **Stock Levels**: Monitor inventory by warehouse
- **Stock Movements**: Audit trail of all inventory movements

### 5. Accounts Payable
- **AP Invoice Processing**: Create and manage invoices
- **3-Way Matching**: Automatic matching of:
  - Purchase Orders
  - Goods Receipts
  - Invoices
  - With configurable tolerance (default 1%)
- Payment tracking

### 6. User Management & Roles
- Custom user model with role-based access control
- **Roles**:
  - Administrator: Full system access
  - Supply Chain Manager: PPO creation, approvals, GRPO posting
  - Buyer: PPO creation
  - Warehouse Staff: GRPO creation and receipt
  - Finance/AP: Invoice processing
  - Viewer: Read-only access

## Project Structure

```
erp_system/
├── manage.py                      # Django management script
├── requirements.txt              # Python dependencies
├── SETUP.md                       # Setup instructions
├── README.md                      # This file
│
├── erp/                           # Main Django project
│   ├── settings.py               # Project settings
│   ├── urls.py                   # Main URL router
│   ├── wsgi.py                   # WSGI config
│   └── asgi.py                   # ASGI config
│
├── accounts/                      # User authentication
│   ├── models.py                 # Custom User model
│   ├── admin.py                  # Django admin config
│   ├── views.py                  # Login/Logout views
│   ├── forms.py                  # User forms
│   └── urls.py                   # Auth URLs
│
├── core/                          # Shared utilities
│   ├── models.py                 # Base model classes
│   ├── utils.py                  # Helper functions
│   └── context_processors.py     # Template context
│
├── items/                         # Item master data
│   ├── models.py                 # Item model
│   ├── admin.py                  # Admin interface
│   ├── views.py                  # CRUD views
│   ├── forms.py                  # Item forms
│   └── urls.py                   # Item URLs
│
├── vendors/                       # Vendor management
│   ├── models.py                 # Vendor, BillTo, ShipTo models
│   ├── admin.py                  # Admin interface
│   ├── views.py                  # CRUD views
│   ├── forms.py                  # Vendor forms
│   └── urls.py                   # Vendor URLs
│
├── procurement/                   # Procurement (PR, PPO, PI)
│   ├── models.py                 # PR, PPO, PI models
│   ├── admin.py                  # Admin interface
│   ├── views.py                  # CRUD views
│   ├── forms.py                  # Procurement forms
│   ├── pdf_generator.py         # PPO PDF generation
│   └── urls.py                   # Procurement URLs
│
├── receiving/                     # Goods receipt (GRPO)
│   ├── models.py                 # GRPO models
│   ├── admin.py                  # Admin interface
│   ├── views.py                  # CRUD views
│   ├── forms.py                  # GRPO forms
│   └── urls.py                   # Receiving URLs
│
├── inventory/                     # Warehouse & stock
│   ├── models.py                 # Warehouse, StockLevel, StockMovement
│   ├── admin.py                  # Admin interface
│   ├── views.py                  # CRUD views
│   ├── forms.py                  # Inventory forms
│   └── urls.py                   # Inventory URLs
│
├── invoicing/                     # AP Invoice processing
│   ├── models.py                 # APInvoice models
│   ├── admin.py                  # Admin interface
│   ├── views.py                  # CRUD views
│   ├── forms.py                  # Invoice forms
│   └── urls.py                   # Invoicing URLs
│
├── templates/                     # HTML templates
│   ├── base.html                 # Base template with navigation
│   ├── dashboard.html            # Dashboard
│   ├── registration/             # Auth templates
│   ├── items/                    # Item templates
│   ├── vendors/                  # Vendor templates
│   ├── procurement/              # Procurement templates
│   ├── receiving/                # Receiving templates
│   ├── inventory/                # Inventory templates
│   └── invoicing/                # Invoicing templates
│
└── static/                        # Static files
    ├── css/
    ├── js/
```

## Database Models

### accounts.User
Custom authentication user with role-based permissions.

### items.Item
Master item database with:
- Item number (unique)
- Description, branch, classification
- Inventory tracking
- Carton and CBM calculations

### vendors.Vendor
Vendor master with contact, payment, and logistics information.

### vendors.BillToAddress
Bill-to addresses for purchase orders.

### vendors.ShipToAddress
Ship-to addresses for deliveries.

### procurement.PurchaseRequisition
Purchase requisition with multiple line items.

### procurement.PlannedPurchaseOrder (PPO)
Main procurement document with:
- Auto-numbered (3149+)
- Multiple status states (Draft → Confirmed → Received → Closed)
- Line items with auto-calculated totals
- Transport and incoterm specifications

### procurement.PPOLineItem
Individual line in a PPO with:
- Item reference
- Quantity and unit price
- Auto-calculated cartons and CBM
- Destination tracking

### procurement.ProformaInvoice
Vendor PI tracking with upload capability.

### receiving.GoodsReceiptPO (GRPO)
Goods receipt document with:
- Auto-numbered (1001+)
- Line-by-line receiving
- Damage tracking
- Batch and expiry tracking

### inventory.Warehouse
Warehouse/location master.

### inventory.StockLevel
Stock quantity per item per warehouse with reorder points.

### inventory.StockMovement
Complete audit trail of all stock movements.

### invoicing.APInvoice
AP invoice with 3-way matching capability.

## Getting Started

### Requirements
- Python 3.8+
- Django 4.2+
- SQLite or PostgreSQL

### Installation

1. **Clone or navigate to the project**
   ```bash
   cd /sessions/hopeful-ecstatic-mendel/mnt/ProcurementSystem/erp_system
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py shell
   >>> from accounts.models import User
   >>> User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')
   >>> exit()
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the system**
   - Dashboard: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Default credentials: `admin` / `admin123`

## Key URLs

| URL | Purpose |
|-----|---------|
| `/` | Dashboard |
| `/login/` | User login |
| `/items/` | Item master list |
| `/vendors/` | Vendor management |
| `/procurement/ppos/` | Purchase Orders |
| `/procurement/requisitions/` | Purchase Requisitions |
| `/procurement/proforma-invoices/` | Proforma Invoices |
| `/receiving/` | Goods Receipts |
| `/inventory/warehouses/` | Warehouse management |
| `/inventory/stock-levels/` | Stock level tracking |
| `/invoicing/` | AP Invoice processing |
| `/admin/` | Django admin interface |

## Workflow Examples

### Creating a Purchase Order

1. Create a Purchase Requisition in `/procurement/requisitions/`
2. Navigate to `/procurement/ppos/create/`
3. Fill in vendor, addresses, incoterms, and line items
4. Items auto-calculate cartons and CBM based on master data
5. Review totals and save
6. Change status from Draft to Sent to Vendor

### Receiving Goods

1. Create GRPO at `/receiving/create/`
2. Reference the PPO
3. Enter received quantities for each line
4. Track any damages or discrepancies
5. Post the GRPO

### Invoice Processing

1. Create AP Invoice at `/invoicing/create/`
2. Reference the PPO and GRPO
3. Enter invoice details
4. System automatically attempts 3-way matching
5. Approve for payment

## Features for Tommy

As Supply Chain Manager, Tommy has access to:

- ✅ Create and manage all procurement documents (PR, PPO, PI)
- ✅ Approve purchase requisitions
- ✅ Post goods receipts
- ✅ View complete order status and history
- ✅ Track delivery dates and shipping information
- ✅ Receive AP invoice notifications
- ✅ Export reports (requires custom development)
- ✅ Manage vendors and addresses
- ✅ Set up new items with auto-calculations

## Admin Access

The Django admin at `/admin/` provides:

- Full CRUD for all models
- Inline editing (e.g., PPO line items)
- Filtering and search across all entities
- User and role management
- System configuration

## Customization

### Adding a Custom Field

1. Edit the model in `<app>/models.py`
2. Create migration: `python manage.py makemigrations <app>`
3. Apply migration: `python manage.py migrate`
4. Update forms in `<app>/forms.py`
5. Update templates as needed

### Extending PPO Calculations

Edit `procurement/models.py` → `PlannedPurchaseOrder.recalculate_totals()` method.

### Changing Number Sequences

Edit `get_next_*_number()` class methods in each model.

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure allowed hosts
3. Use PostgreSQL instead of SQLite
4. Set up static files collection: `python manage.py collectstatic`
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Configure HTTPS/SSL
7. Set up database backups
8. Configure email for notifications (optional)

## Support & Maintenance

- All code is fully documented
- Models follow Django best practices
- Admin interface is fully configured for all models
- Audit trails on key documents (timestamps, user tracking)

## License

Internal use only - Michael Todd Beauty, Inc.

---

**Built with Django 4.2 | SQLite Database | Bootstrap 5 UI**
