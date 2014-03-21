from handler import Handler
from models import *

from lib import utils

class TestBidHandler(Handler):
    def get(self):
        # company = Company.get_by_ein("12345")
        # company.apr = 9.0
        # company.put()

        # username = 'admin'
        # password = 'pass'

        # password = utils.hashing(password, self.app.config.get('salt'))

        # unique_properties = ['username']
        # auth_id = "own:%s" % username
        # user = self.auth.store.user_model.create_user(
        #     auth_id, unique_properties, password_raw=password,
        #     username=username, ip=self.request.remote_addr
        # )

        par = OfferParameters()
        par.buyer_id = "5676830073815040"
        par.supplier_id = "5676830073815040"
        par.parameters_type = "Ask"

        par.alt_1_percent = 1.0
        par.alt_2_percent = 2.0
        par.alt_3_percent = 3.0

        par.alt_1_days = 10
        par.alt_2_days = 20
        par.alt_3_days = 30

        par.put()
        
        # company = Company()
        # company.username = "admin"
        # company.password = "pass"

        # company.put()

        # bid = Bid()
        # bid.inv_id = "5724160613416960"
        # bid.discount = 12.3
        # bid.days_acc = 20
        # bid.amount = 12.34
        # bid.status = "Accepted"
        # bid.profit = 54.34
        # bid.apr = 1.2
        # bid.is_standing_offer = True

        # invoice = Invoice.get_by_id(5724160613416960)

        # bid.put()

        # invoice.recent_bid = bid.key
        # invoice.put()

        self.write("Done")