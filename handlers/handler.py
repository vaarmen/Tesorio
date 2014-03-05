import webapp2
import os
import jinja2
import logging

import hashlib
from datetime import timedelta

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

from config import config

template_dir = os.path.join(os.path.dirname(__file__), '../')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True, extensions=['jinja2.ext.with_'])

COMPANIES_DICT = {
    "5629499534213120": "Admin Company"
}

class Handler(webapp2.RequestHandler):
    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in
        config['webapp2_extras.auth']['user_attributes'].
        :returns
        A dictionary with most user information
        """
        return self.auth.get_user_by_session()
 
    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
        The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """   
        return self.auth.store.user_model

    @webapp2.cached_property
    def current_user(self):
        """Returns User model from App Engine datastore"""
        user = self.auth.get_user_by_session()
        if user:
            return models.User.get_by_id(user['user_id'])
        return None
 
    @webapp2.cached_property
    def session(self):
      """Shortcut to access the current session."""
      return self.session_store.get_session(backend="datastore")

    @webapp2.cached_property
    def get_company(self):
        """Returns Company reference from User"""
        return self.user.company.get() if self.user else None

    @webapp2.cached_property
    def get_company_id(self):
        """Returns entity id for user company"""
        return self.user.company.id if self.user else None
 
    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
        'message': message
        }
        self.render_template('message.html', params)
 
    # this is needed for webapp2 sessions to work
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        user = self.user_info
        kw['user'] = user

        kw['company'] = self.get_company

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

def get_company_name(company_id):
    return COMPANIES_DICT[company_id]

jinja_env.filters['format_currency'] = format_currency
jinja_env.filters['format_date'] = format_date
jinja_env.globals['calculate_discount'] = calculate_discount
jinja_env.globals['calculate_date'] = calculate_date
jinja_env.globals['get_company_name'] = get_company_name