import webapp2
import os
import jinja2
import logging

import hashlib

template_dir = os.path.join(os.path.dirname(__file__), '../')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True, extensions=['jinja2.ext.with_'])

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

def cookie_validation(self, cookie):
    if not cookie or cookie == '':
        self.redirect('/login')
        return

    [company_id, company_hash] = cookie.split("|")

    if not valid_cookie(company_id, company_hash):
        logging.error("Error: Invalid Cookie")
        logging.error("Company ID: " + company_id)
        logging.error("Company Hash: " + company_hash)
        self.redirect('/login')
        return
    
def valid_cookie(company_id, company_hash):
    return company_hash == hashlib.sha1(company_id).hexdigest()