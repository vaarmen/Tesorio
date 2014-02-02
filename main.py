import webapp2
from handlers import *

app = webapp2.WSGIApplication([
    ('/', index.IndexHandler),
    ('/upload/company', upload_company.UploadCompanyHandler),
    ('/upload/invoice', upload_invoice.UploadInvoiceHandler)
], debug=True)
