import webapp2
from handlers import *

app = webapp2.WSGIApplication([
    ('/', index.IndexHandler),
    ('/panel/input/company', input_company.InputCompanyHandler),
    ('/panel/input/invoice', input_invoice.InputInvoiceHandler),
    ('/login', login.LoginHandler)
], debug=True)
