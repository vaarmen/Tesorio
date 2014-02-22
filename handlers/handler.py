import webapp2
import os
import jinja2
import logging

import hashlib
from datetime import timedelta

template_dir = os.path.join(os.path.dirname(__file__), '../')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True, extensions=['jinja2.ext.with_'])

COMPANIES_DICT = {
    "5629499534213120": "Admin Company"
}

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

## Returns True if cookie is validated
def cookie_validation(self, cookie):
    if not cookie or cookie == '':
        self.redirect('/login')
        return False

    [company_id, company_hash] = cookie.split("|")

    if not valid_cookie(company_id, company_hash):
        logging.error("Error: Invalid Cookie")
        logging.error("Company ID: " + company_id)
        logging.error("Company Hash: " + company_hash)
        self.redirect('/login')
        return False

    return True
    
def valid_cookie(company_id, company_hash):
    return company_hash == hashlib.sha1(company_id).hexdigest()

## Formats currency in Jinja2
def format_currency(value):
    return "${:,.2f}".format(value)

def format_date(date):
    return date.strftime('%m-%d-%Y')

def calculate_discount(amount, discount):
    logging.info(amount)
    logging.info(discount)
    return (100 - discount)/100 * amount

def calculate_date(date, days):
    return date - timedelta(days=days)

jinja_env.filters['format_currency'] = format_currency
jinja_env.filters['format_date'] = format_date
jinja_env.globals['calculate_discount'] = calculate_discount
jinja_env.globals['calculate_date'] = calculate_date