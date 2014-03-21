import webapp2
from handlers import *
from config import config

## Create contact page

# Add to base body later
# {% with company=company %}
#   {% include "/views/base/navbar.html" %}
#   {% endwith %}

app = webapp2.WSGIApplication([
    ('/', index.IndexHandler),
    ('/login', login.LoginHandler),
    ('/logout', logout.LogoutHandler),

    ('/panel', home_panel.HomePanelHandler),
    ('/panel/buyer', buyer_panel.BuyerPanelHandler),
    ('/panel/supplier', supplier_panel.SupplierPanelHandler),
    ('/panel/input/company', input_company.InputCompanyHandler),
    ('/panel/input/invoice', input_invoice.InputInvoiceHandler),

    ('/panel/invoice', invoice.InvoiceRedirectHandler),
    ('/panel/invoice/(\d+)', invoice.InvoiceHandler),

    ('/test', testbid.TestBidHandler)
], debug=True, config=config)
