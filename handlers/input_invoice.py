from handler import Handler
from handler import cookie_validation
import models
from datetime import datetime

from lib.decorators import user_required

import logging

class InputInvoiceHandler(Handler):
    @user_required
    def get(self):
        self.render("/views/input-invoice.html")

    @user_required
    def post(self):
        # Request form input
        buyer_id = self.request.get("buyer-id")
        supplier_id = self.request.get("supplier-id")
        buyer_inv_key = self.request.get("binvoice-key")
        supplier_inv_number = self.request.get("sinvoice-number")
        amount = self.request.get("amount")
        inv_date = self.request.get("invoice-date")
        due_date = self.request.get("due-date")
        po_num = self.request.get("purchase-order")
        description = self.request.get("description")
        date_approved = self.request.get("date-approved")

        # Validate buyer_id & supplier_id
        if not valid_id(buyer_id):
            logging.error("Invalid Buyer ID while inputting invoice: " + buyer_id)
            self.write("Invalid Buyer ID: " + buyer_id)
            return

        if not valid_id(supplier_id):
            logging.error("Invalid Supplier ID while inputting invoice: " + supplier_id)
            self.write("Invalid Supplier ID: " + supplier_id)
            return
        
        # Log all form input
        logging.info("UploadInvoiceHandler POST Method Logs")
        logging.info("Buyer Tesorio ID: " + buyer_id)
        logging.info("Supplier Tesorio ID: " + supplier_id)
        logging.info("Buyer Invoice Key: " + buyer_inv_key)
        logging.info("Supplier Invoice Number: " + supplier_inv_number)
        logging.info("Amount: " + amount)
        logging.info("Invoice Date: " + inv_date)
        logging.info("Due Date: " + due_date)
        logging.info("Purchase Order Number: " + po_num)
        logging.info("Line Items/Description: " + description)
        logging.info("Date Approved: " + date_approved)

        # Put form input into model and database
        invoice = models.Invoice()
        invoice.buyer_id = buyer_id
        invoice.supplier_id = supplier_id
        invoice.buyer_inv_key = buyer_inv_key
        invoice.supplier_inv_number = supplier_inv_number
        invoice.amount = float(amount)
        invoice.inv_date = datetime.strptime(inv_date, '%m/%d/%Y')
        invoice.due_date = datetime.strptime(due_date, '%m/%d/%Y')
        invoice.po_num = po_num
        invoice.description = description
        invoice.date_approved = datetime.strptime(date_approved, '%m/%d/%Y')

        invoice.put()

        self.render("/views/input-invoice.html", success=True)

def valid_id(company_id):
    if not company_id or company_id == '':
        return False

    company_id = int(company_id)
    company = models.Company.get_by_id(company_id)

    if company:
        return True
    else:
        return False