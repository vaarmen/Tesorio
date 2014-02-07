from handler import Handler
from models import Company
import logging

import hashlib

class LoginHandler(Handler):
    def get(self):
        self.render("/html/login.html")

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        query = Company.query(Company.username == username).get()
        
        if not query:
            logging.error("Error: Invalid username")
            logging.error("Username: " + username)
            logging.error("Password: " + password)
            self.render("/html/login.html", username_error="form-control-error", username=username)

        elif not password == query.password:
            logging.error("Error: Invalid password")
            logging.error("Username: " + username)
            logging.error("Password: " + password)

            self.render("/html/login.html", password_error="form-control-error", username=username)

        # Successful login
        else:
            # Generate login cookie
            login_cookie = generate_cookie(query.key.id())

            logging.info("Successful login")
            logging.info("Username: " + username)
            logging.info("Password: " + password)
            logging.info("Cookie: " + login_cookie)

            # Set cookie
            self.response.set_cookie('login', login_cookie, path='/')

            self.redirect('/panel/input/company')

def generate_cookie(company_id):
    company_id = str(company_id)
    id_hash = hashlib.sha1(company_id).hexdigest()
    return company_id + "|" + id_hash