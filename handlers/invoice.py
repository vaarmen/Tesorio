from handler import Handler
from handler import cookie_validation

from models import Company, Invoice, OfferParameters

import logging

# Used for redirecting url /panel/invoice without id
class InvoiceRedirectHandler(Handler):
    def get(self):
        self.redirect('/panel')

class InvoiceHandler(Handler):
    def get(self, invoice_id):
        cookie = self.request.cookies.get('login')
        if not cookie_validation(self, cookie):
            return

        option = self.request.get('option')
        invoice = Invoice.get_by_id(int(invoice_id))
        company_id = cookie.split("|")[0]
        company = Company.get_by_id(int(company_id))

        if not invoice:
            logging.error("Tried accessing invalid invoice: #" + invoice_id)
            self.render("/views/invoice.html", invalid=True, invoice_id=invoice_id, company=company)
            return

        parameters = OfferParameters.query(OfferParameters.buyer_id == invoice.buyer_id, OfferParameters.supplier_id == invoice.supplier_id).get()
        
        ## Fix this later
        if not parameters:
            logging.error("OfferParameters not found")
            logging.error("buyer_id: " + invoice.buyer_id)
            logging.error("supplier_id: " + invoice.supplier_id)
            self.write("Bad parameters")
            return
        
        if invoice.supplier_id == company_id:
            self.render("/views/invoice.html", supplier=True, invoice=invoice, invoice_id=invoice_id, company=company, option=option, parameters=parameters)

        elif invoice.buyer_id == company_id:
            self.render("/views/invoice.html", buyer=True, invoice=invoice, invoice_id=invoice_id, company=company, parameters=parameters)

        else:
            logging.error("Error: " + company_id + " tried to access invoice #" + invoice_id)     
            self.render("/views/invoice.html", invalid=True, invoice_id=invoice_id, company=company)

    def post(self, invoice_id):
        cookie = self.request.cookies.get('login')
        if not cookie_validation(self, cookie):
            return

        ## Do verification on these and offer parameters
        discount = self.request.get('discount')
        days_acc = self.request.get('days-acc')

        self.write(discount + days_acc)