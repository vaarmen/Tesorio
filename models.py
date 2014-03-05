import time

from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User
from webapp2_extras import security

class User(User):
    name = ndb.StringProperty() ## don't know why I need this, need to remove later

    username = ndb.StringProperty()
    password = ndb.StringProperty()

    company = ndb.KeyProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    def get_company(self):
        return self.company.get() if self.company else None

    # def set_password(self, raw_password):
    #     """Sets the password for the current user

    #     :param raw_password:
    #     The raw password which will be hashed and stored
    #     """
    #     self.password = security.generate_password_hash(raw_password, length=12)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
        The user_id of the requesting user.
        :param token:
        The token string to be verified.
        :returns:
        A tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

            return None, None

    @classmethod
    def get_by_username(cls, username):
        """Returns a user object based on an username.

        :param username:
            String representing the username.

        :returns:
            A user object.
        """

        return cls.query(cls.username == username).get()

class Company(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()

    authorized_users = ndb.KeyProperty(kind=User, repeated=True)
    registered = ndb.BooleanProperty()
    ein = ndb.StringProperty()

    name = ndb.StringProperty()
    is_buyer = ndb.BooleanProperty()
    is_supplier = ndb.BooleanProperty()

    ## Address class?
    address = ndb.StringProperty()

    company_phone = ndb.StringProperty()
    company_email = ndb.StringProperty()

    ## Perhaps Contact class
    contact_person = ndb.StringProperty()
    contact_phone = ndb.StringProperty()
    contact_email = ndb.StringProperty()

    suppliers = ndb.KeyProperty(repeated=True)
    buyers = ndb.KeyProperty(repeated=True)

    ## Need to be changed to see changes
    cash_committed = ndb.FloatProperty()
    apr = ndb.FloatProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

class Offer(ndb.Model):
    invoice_ref = ndb.KeyProperty()
    offer_type = ndb.StringProperty(choices=["Bid", "Ask"])
    parameters_ref = ndb.KeyProperty()

    discount = ndb.FloatProperty()

    days_acc = ndb.IntegerProperty()
    date_due = ndb.DateProperty()
    amount = ndb.FloatProperty()

    status = ndb.StringProperty(choices=["Cleared", "Pending", "Declined"])
    profit = ndb.FloatProperty()
    apr = ndb.FloatProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

## TesorioUser account
## With email (as username), password, permissions, company_id
## Link Company with authorized_user_list

## Mapping class for when getting info from invoice
## Perhaps make a class that can do methods that do that
## Like methods such as invoice.get_company_name() etc...
## Abstract away this

## Messages class. All sent messages on our server
## from, to, subject, message
## type_of_message = company_support, web_contact, offers, supplier_invite, buyer_invite, payment_instructions
## resolved = boolean

## Finance class. Needed for when payments made from offer
## When cash committed changes or apr.

class OfferParameters(ndb.Model):
    buyer_id = ndb.StringProperty()
    supplier_id = ndb.StringProperty()
    parameters_type = ndb.StringProperty(choices=["Bid", "Ask"])

    alt_1_percent = ndb.FloatProperty()
    alt_2_percent = ndb.FloatProperty()
    alt_3_percent = ndb.FloatProperty()

    alt_1_days = ndb.IntegerProperty()
    alt_2_days = ndb.IntegerProperty()
    alt_3_days = ndb.IntegerProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

class Invoice(ndb.Model):
    buyer_id = ndb.StringProperty()
    supplier_id = ndb.StringProperty()

    ## Possibly change structure to KeyProperty
    buyer_inv_key = ndb.StringProperty()
    supplier_inv_number = ndb.StringProperty()

    # Recent bid. Could have been declined or accepted.
    recent_bid = ndb.KeyProperty(kind=Offer)
    status = ndb.StringProperty(choices=["Cleared", "Pending", "Expired", "Open", "Canceled"])

    amount = ndb.FloatProperty()

    inv_date = ndb.DateProperty()
    due_date = ndb.DateProperty()

    po_num = ndb.StringProperty()
    description = ndb.TextProperty()

    date_approved = ndb.DateProperty()
    
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)