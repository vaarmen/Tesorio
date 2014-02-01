from google.appengine.ext import db

class Company(db.Model):
    company_key = db.StringProperty()
    username = db.StringProperty()
    password = db.StringProperty()

    name = db.StringProperty()
    is_buyer = db.BooleanProperty()
    is_supplier = db.BooleanProperty()
    address = db.StringProperty()
    tax_id = db.StringProperty()
    company_phone = db.PhoneNumberProperty()
    company_email = db.EmailProperty()

    contact_person = db.StringProperty()
    contact_phone = db.PhoneNumberProperty()
    contact_email = db.EmailProperty()

    suppliers = db.StringListProperty()
    buyers = db.StringListProperty()

    cash_committed = db.FloatProperty()
    apr = db.FloatProperty()

class Invoice(db.Model):
    inv_key = db.StringProperty()
    buyer_key = db.StringProperty()
    supplier_key = db.StringProperty()

    buyer_inv_key = db.StringProperty()
    supplier_inv_key = db.StringProperty()

    amount = db.FloatProperty()

    inv_date = db.DateTimeProperty()
    due_date = db.DateTimeProperty()

    po_num = db.StringProperty()
    description = db.TextProperty()

    date_approved = db.DateTimeProperty()
    date_uploaded = db.DateTimeProperty()

class Bid(db.Model):
    bid_key = db.StringProperty()
    inv_key = db.StringProperty()

    discount = db.FloatProperty()

    days_acc = db.IntegerProperty()
    date_due = db.DateTimeProperty() # date need cash by
    amount = db.FloatProperty()

    is_standing_offer = db.BooleanProperty()
    date_submit = db.DateTimeProperty()