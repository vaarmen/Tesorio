from handler import Handler
from handler import cookie_validation
from models import Company
from models import Invoice

import logging

companies = {
	"5891733057437696": "Tesorio"
}

class PanelHandler(Handler):
    def get(self):
        cookie = self.request.cookies.get('login')
        cookie_validation(self, cookie)

        company_id = cookie.split("|")[0]
        company_id = int(company_id)
        company = Company.get_by_id(company_id)

        invoices = Invoice.query(Invoice.buyer_id == str(company_id))

        self.render("/html/panel.html", company=company, companies=companies, invoices=invoices)