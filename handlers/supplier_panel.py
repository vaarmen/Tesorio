from handler import Handler
from handler import cookie_validation
from models import Company
from models import Invoice

from lib.decorators import user_required

import logging

companies = {
	"5649050225344512": "Tesorio Company"
}

class SupplierPanelHandler(Handler):
    @user_required
    def get(self):
        company_id = self.get_company_id()

        invoices = Invoice.query(Invoice.supplier_id == str(company_id))
        # Calculate returns
        # Total from invoices where Status = "Accepted"
        # Count invoices and sum total profit

        # Cash Pool
        # Get invoices where status is accepted
        # Bid amount to be paid
        # Cash committed - bid amount paid for available cash

        # invoices
        # Total available is NOT accepted or expired
        # Count # of unique suppliers from invoice query
        # The % one is pending and Open BD. Count # of unique suppliers and divide by total # of suppliers

        self.render("/views/supplier-panel.html", invoices=invoices)