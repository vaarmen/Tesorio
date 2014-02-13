from handler import Handler
from handler import cookie_validation
from models import Company
from models import Invoice

import logging

class HomePanelHandler(Handler):
    def get(self):
        cookie = self.request.cookies.get('login')
        if not cookie_validation(self, cookie):
            return

        company_id = cookie.split("|")[0]
        company_id = int(company_id)
        company = Company.get_by_id(company_id)

        self.render("/html/home-panel.html", company=company)