from handler import Handler
from models import User
import logging

import hashlib

from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError

from lib import utils


class LoginHandler(Handler):
    def get(self):
        self.render('/views/login.html')

    def post(self):
        try:
            username = self.request.get('username')
            password = self.request.get('password')

            user = User.get_by_username(username)

            if not user:
                self.render('/views/login.html', invalid=True)
                return

            else:
                auth_id = user.auth_ids[0]

                password = utils.hashing(password, self.app.config.get('salt'))

                self.auth.get_user_by_password(auth_id, password)

                self.redirect('/panel')

        except (InvalidAuthIdError, InvalidPasswordError), e:
            self.render('/views/login.html', invalid=True)

    # def post(self):
    #     username = self.request.get('username')
    #     password = self.request.get('password')

    #     query = Company.query(Company.username == username).get()
        
    #     if not query:
    #         logging.error("Error: Invalid username")
    #         logging.error("Username: " + username)
    #         logging.error("Password: " + password)
    #         self.render("/views/login.html", username_error="form-control-error", username=username)

    #     elif not password == query.password:
    #         logging.error("Error: Invalid password")
    #         logging.error("Username: " + username)
    #         logging.error("Password: " + password)

    #         self.render("/views/login.html", password_error="form-control-error", username=username)

    #     # Successful login
    #     else:
    #         # Generate login cookie
    #         login_cookie = generate_cookie(query.key.id())

    #         logging.info("Successful login")
    #         logging.info("Username: " + username)
    #         logging.info("Password: " + password)
    #         logging.info("Cookie: " + login_cookie)

    #         # Set cookie
    #         self.response.set_cookie('login', login_cookie, path='/')

    #         self.redirect('/panel')

def generate_cookie(company_id):
    company_id = str(company_id)
    id_hash = hashlib.sha1(company_id).hexdigest()
    return company_id + "|" + id_hash