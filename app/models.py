# stdlib
import datetime

# django
from django.db import models
from django.contrib.auth.models import User

# 3rd party
import jsonfield
from south.modelsinspector import add_introspection_rules
from simple_history.models import HistoricalRecords


# alex did this, and he can't remember why =)
add_introspection_rules([], [
  "^jsonfield\.JSONField"])

OFFER_TYPES = (
    ('BID', 'Bid'),
    ('ASK', 'Ask')
)

OFFER_STATUSES = (
    ('CLEARED', 'Cleared'),
    ('PENDING', 'Pending'),
    ('DECLINED', 'Declined')
)

INVOICE_STATUSES = (
    ('CLEARED', 'Cleared'),
    ('PENDING', 'Pending'),
    ('EXPIRED', 'Expired'),
    ('OPEN', 'Open'),
    ('CANCELED', 'Canceled')
)

TIMEZONE_CHOICES = (
  ### for tz in pytz.country_timezones('US'):
  ###   print '("'+tz+'", "'+str(tz.split('/',1)[1]).replace("_"," ")+'"),'
  ("America/New_York", "New York"),
  ("America/Detroit", "Detroit"),
  ("America/Kentucky/Louisville", "Kentucky/Louisville"),
  ("America/Kentucky/Monticello", "Kentucky/Monticello"),
  ("America/Indiana/Indianapolis", "Indiana/Indianapolis"),
  ("America/Indiana/Vincennes", "Indiana/Vincennes"),
  ("America/Indiana/Winamac", "Indiana/Winamac"),
  ("America/Indiana/Marengo", "Indiana/Marengo"),
  ("America/Indiana/Petersburg", "Indiana/Petersburg"),
  ("America/Indiana/Vevay", "Indiana/Vevay"),
  ("America/Chicago", "Chicago"),
  ("America/Indiana/Tell_City", "Indiana/Tell City"),
  ("America/Indiana/Knox", "Indiana/Knox"),
  ("America/Menominee", "Menominee"),
  ("America/North_Dakota/Center", "North Dakota/Center"),
  ("America/North_Dakota/New_Salem", "North Dakota/New Salem"),
  ("America/North_Dakota/Beulah", "North Dakota/Beulah"),
  ("America/Denver", "Denver"),
  ("America/Boise", "Boise"),
  ("America/Shiprock", "Shiprock"),
  ("America/Phoenix", "Phoenix"),
  ("America/Los_Angeles", "Los Angeles"),
  ("America/Anchorage", "Anchorage"),
  ("America/Juneau", "Juneau"),
  ("America/Sitka", "Sitka"),
  ("America/Yakutat", "Yakutat"),
  ("America/Nome", "Nome"),
  ("America/Adak", "Adak"),
  ("America/Metlakatla", "Metlakatla"),
  ("Pacific/Honolulu", "Honolulu"),
)


class Person(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='person')
    company = models.ForeignKey('Company', related_name='people')

    settings = jsonfield.JSONField(default={})
    time_zone = models.CharField(max_length=100,
        choices=TIMEZONE_CHOICES, default="America/New_York")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Company(models.Model):
    name = models.CharField(max_length=254, blank=True)
    ein = models.CharField(max_length=254, blank=True)

    address = models.TextField(blank=True)  # Address class?
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    has_registered = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    # this can be changed to be the reverse, it doesnt make a difference
    buyers = models.ManyToManyField('self',
        symmetrical=False, related_name='suppliers')
    cash_commited = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    apr = models.DecimalField(default=0, max_digits=20, decimal_places=5)

    settings = jsonfield.JSONField(default={})
    history = HistoricalRecords()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Offer(models.Model):
    invoice = models.ForeignKey('Invoice')
    offer_type = models.CharField(max_length=254, choices=OFFER_TYPES, default='BID')
    parameters = models.ForeignKey('OfferParameters', related_name='offers')

    discount = models.DecimalField(default=0, max_digits=11, decimal_places=10)

    days_accelerated = models.IntegerField()
    date_due = models.DateTimeField()

    amount = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    status = models.CharField(max_length=254, choices=OFFER_STATUSES)
    profit = models.DecimalField(default=0, max_digits=20, decimal_places=4)
    apr = models.DecimalField(default=0, max_digits=20, decimal_places=5)

    settings = jsonfield.JSONField(default={})
    history = HistoricalRecords()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class OfferParameters(models.Model):
    buyer = models.ForeignKey(Company, related_name='buyer_offerparams')
    supplier = models.ForeignKey(Company, related_name='supplier_offerparams')
    parameters_type = models.CharField(max_length=254, choices=OFFER_TYPES, default='BID')


    alt_1_percent = models.DecimalField(max_digits=20, decimal_places=5)
    alt_2_percent = models.DecimalField(max_digits=20, decimal_places=5)
    alt_3_percent = models.DecimalField(max_digits=20, decimal_places=5)

    alt_1_days = models.IntegerField()
    alt_2_days = models.IntegerField()
    alt_3_days = models.IntegerField()

    settings = jsonfield.JSONField(default={})
    history = HistoricalRecords()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Invoice(models.Model):
    buyer = models.ForeignKey(Company, related_name='buyer_invoices')
    supplier = models.ForeignKey(Company, related_name='supplier_invoices')

    buyer_inv_key = models.CharField(max_length=1000)
    supplier_inv_number = models.CharField(max_length=1000)

    # Recent bid. Could have been declined or accepted.
    current_bid = models.OneToOneField(Offer, related_name='current_invoice')
    status = models.CharField(max_length=254, choices=INVOICE_STATUSES, default='OPEN')

    amount = models.DecimalField(default=0, max_digits=20, decimal_places=4)

    inv_date = models.DateField()
    due_date = models.DateField()

    po_num = models.CharField(max_length=1000, blank=True)
    description = models.TextField()

    date_approved = models.DateTimeField()

    settings = jsonfield.JSONField(default={})
    history = HistoricalRecords()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
