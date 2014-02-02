from handler import Handler
import models
from datetime import datetime

import logging

class UploadInvoiceHandler(Handler):
    def get(self):
        self.render("/html/upload-invoice.html")

    def post(self):
        # Request form input
        buyer_inv_key = self.request.get("binvoice-key")
        supplier_inv_number = self.request.get("sinvoice-number")
        amount = self.request.get("amount")
        inv_date = self.request.get("invoice-date")
        due_date = self.request.get("due-date")
        po_num = self.request.get("purchase-order")
        description = self.request.get("description")
        date_approved = self.request.get("date-approved")
        
        # Log all form input
        logging.info("UploadInvoiceHandler POST Method Logs")
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
        invoice.buyer_inv_key = buyer_inv_key
        invoice.supplier_inv_number = supplier_inv_number
        invoice.amount = float(amount)
        invoice.inv_date = datetime.strptime(inv_date, '%m/%d/%Y')
        invoice.due_date = datetime.strptime(due_date, '%m/%d/%Y')
        invoice.po_num = po_num
        invoice.description = description
        invoice.date_approved = datetime.strptime(date_approved, '%m/%d/%Y')

        invoice.put()

        self.write("Done")