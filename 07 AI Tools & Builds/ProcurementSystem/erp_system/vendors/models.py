from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Vendor(models.Model):
    name = models.CharField(max_length=300, db_index=True)
    code = models.CharField(max_length=50, blank=True, db_index=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    lead_time_days = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)],
        help_text="Default lead time in days",
    )
    currency = models.CharField(max_length=3, default='USD')
    wire_info = models.TextField(blank=True, help_text="Bank/wire transfer details")
    default_port_of_loading = models.CharField(max_length=200, blank=True, help_text="Default port of loading for PPOs")
    default_country_of_origin = models.CharField(max_length=100, blank=True, help_text="Default country of origin for PPOs")
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    rating = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1-5 star rating",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Branch(models.Model):
    """Company branches: Michael Todd Beauty, Spa Sciences, NasalFresh MD"""
    name = models.CharField(max_length=200, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Branches"
        ordering = ['name']

    def __str__(self):
        return self.name


class BillToAddress(models.Model):
    branch = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Bill-To Addresses"

    def __str__(self):
        return self.branch


class ThreePLProvider(models.Model):
    """3PL fulfillment partners: ShipBob, Floship, Amazon FBA, etc."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True, help_text="Short code e.g. SB, FS, AMZ")
    address = models.TextField(blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA')
    phone = models.CharField(max_length=50, blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    account_number = models.CharField(max_length=100, blank=True, help_text="Your account # with this 3PL")
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "3PL Provider"
        verbose_name_plural = "3PL Providers"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        parts = [self.address]
        city_state = ', '.join(filter(None, [self.city, self.state]))
        if city_state:
            parts.append(f"{city_state} {self.zip_code}".strip())
        if self.country and self.country != 'USA':
            parts.append(self.country)
        return '\n'.join(parts)


# Keep ShipToAddress for backwards compatibility but it's now secondary to ThreePLProvider
class ShipToAddress(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='USA')
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Ship-To Addresses"

    def __str__(self):
        return self.name
