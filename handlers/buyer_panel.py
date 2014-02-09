from handler import Handler
from handler import cookie_validation
from models import Company
from models import Invoice

import logging

companies = {
	"5649050225344512": "Tesorio Company"
}

class BuyerPanelHandler(Handler):
    def get(self):
        cookie = self.request.cookies.get('login')
        cookie_validation(self, cookie)

        company_id = cookie.split("|")[0]
        company_id = int(company_id)
        company = Company.get_by_id(company_id)

        invoices = Invoice.query(Invoice.buyer_id == str(company_id))
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

        self.render("/html/buyer-panel.html", company=company, companies=companies, invoices=invoices)