from handler import Handler

from models import Company, Invoice, OfferParameters

from lib.decorators import user_required

import logging

# Used for redirecting url /panel/invoice without id
class InvoiceRedirectHandler(Handler):
    def get(self):
        self.redirect('/panel')

class InvoiceHandler(Handler):
    @user_required
    def get(self, invoice_id):
        option = self.request.get('option')
        invoice = Invoice.get_by_id(int(invoice_id))
        company_id = str(self.get_company_id())
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
        
        if invoice.supplier_id == str(company_id):
            self.render("/views/invoice.html", supplier=True, invoice=invoice, invoice_id=invoice_id, company=company, option=option, parameters=parameters)

        elif invoice.buyer_id == str(company_id):
            self.render("/views/invoice.html", buyer=True, invoice=invoice, invoice_id=invoice_id, company=company, parameters=parameters)

        else:
            logging.error("Error: " + str(company_id) + " tried to access invoice #" + str(invoice_id))     
            self.render("/views/invoice.html", invalid=True, invoice_id=invoice_id, company=company)

    @user_required
    def post(self, invoice_id):
        ## Do verification on these and offer parameters
        discount = self.request.get('discount')
        days_acc = self.request.get('days-acc')

        self.write(discount + days_acc)