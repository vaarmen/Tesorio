from google.appengine.ext import ndb

class Company(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    registered = ndb.BooleanProperty()

    name = ndb.StringProperty()
    is_buyer = ndb.BooleanProperty()
    is_supplier = ndb.BooleanProperty()
    address = ndb.StringProperty()
    tax_id = ndb.StringProperty()
    company_phone = ndb.StringProperty()
    company_email = ndb.StringProperty()

    contact_person = ndb.StringProperty()
    contact_phone = ndb.StringProperty()
    contact_email = ndb.StringProperty()

    supplier = ndb.StringProperty(repeated=True)
    buyer = ndb.StringProperty(repeated=True)

    cash_committed = ndb.FloatProperty()
    apr = ndb.FloatProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)

class Bid(ndb.Model):
    inv_id = ndb.StringProperty()

    discount = ndb.FloatProperty()

    days_acc = ndb.IntegerProperty()
    date_due = ndb.DateProperty()
    amount = ndb.FloatProperty()

    status = ndb.StringProperty(choices=["Accepted", "Pending", "Declined"])
    profit = ndb.FloatProperty()
    apr = ndb.FloatProperty()

    is_standing_offer = ndb.BooleanProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)

class Invoice(ndb.Model):
    buyer_id = ndb.StringProperty()
    supplier_id = ndb.StringProperty()

    buyer_inv_key = ndb.StringProperty()
    supplier_inv_number = ndb.StringProperty()

    recent_bid = ndb.KeyProperty()
    status = ndb.StringProperty(choices=["Accepted", "Pending", "Expired", "Open", "Open BD"])

    amount = ndb.FloatProperty()

    inv_date = ndb.DateProperty()
    due_date = ndb.DateProperty()

    po_num = ndb.StringProperty()
    description = ndb.TextProperty()

    date_approved = ndb.DateProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)