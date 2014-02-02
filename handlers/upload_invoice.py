from handler import Handler
import models
from datetime import datetime

class UploadInvoiceHandler(Handler):
    def get(self):
        self.render("/html/upload-invoice.html")

    def post(self):
        buyer_inv_key = self.request.get("binvoice-key")
        supplier_inv_key = self.request.get("sinvoice-key")
        amount = self.request.get("amount")
        inv_date = self.request.get("invoice-date")
        due_date = self.request.get("due-date")
        po_num = self.request.get("purchase-order")
        description = self.request.get("description")
        date_approved = self.request.get("date-approved")
        
        invoice = models.Invoice()
        invoice.buyer_inv_key = buyer_inv_key
        invoice.supplier_inv_key = supplier_inv_key
        invoice.amount = float(amount)
        invoice.inv_date = datetime.strptime(inv_date, '%m/%d/%Y')
        invoice.due_date = datetime.strptime(due_date, '%m/%d/%Y')
        invoice.po_num = po_num
        invoice.description = description
        invoice.date_approved = datetime.strptime(date_approved, '%m/%d/%Y')

        invoice.put()

        self.write("Done")