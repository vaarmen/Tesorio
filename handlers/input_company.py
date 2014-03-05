from handler import Handler
from handler import cookie_validation
import models

from lib import utils
from lib.decorators import user_required

import logging

class InputCompanyHandler(Handler):
    @user_required
    def get(self):
        self.render("/views/input-company.html")

    @user_required
    def post(self):
        # Request form input
        username = self.request.get('username')
        password = self.request.get('password')
        name = self.request.get('name')
        is_buyer = self.request.get('buyer')
        is_supplier = self.request.get('supplier')
        address = self.request.get('address')
        city = self.request.get('city')
        state = self.request.get('state')
        zip_code = self.request.get('zip')
        ein = self.request.get('ein')
        company_phone = self.request.get('company-phone')
        company_email= self.request.get('company-email')
        contact_person = self.request.get('contact-name')
        contact_phone = self.request.get('contact-phone')
        contact_email = self.request.get('contact-email')

        # Convert to boolean
        if is_buyer: is_buyer = True
        else: is_buyer = False

        if is_supplier: is_supplier = True
        else: is_supplier = False

        # Construct correct address format
        company_address = address + ", " + city + ", " + state + ", " + zip_code

        # Hash password
        password = utils.hashing(password, self.app.config.get('salt'))

        # Log all form input
        logging.info("UploadCompanyHandler POST Method Logs")
        logging.info("Username: " + username)
        logging.info("Company Name: " + name)
        logging.info("Is Buyer: " + str(is_buyer))
        logging.info("Is Supplier: " + str(is_supplier))
        logging.info("Company Address: " + company_address)
        logging.info("EIN: " + ein)
        logging.info("Company Phone: " + company_phone)
        logging.info("Company Email: " + company_email)
        logging.info("Contact Person:" + contact_person)
        logging.info("Contact Person Phone: " + contact_phone)
        logging.info("Comtact Person Email: " + contact_email)
        
        # Put form input into model and database
        company = models.Company()
        company.ein = ein
        company.registered = True
        company.name = name
        company.is_buyer = is_buyer
        company.is_supplier = is_supplier
        company.address = company_address
        company.company_phone = company_phone
        company.company_email = company_email
        company.contact_person = contact_person
        company.contact_phone = contact_phone
        company.contact_email = contact_email

        company.put()

        # Passing password_raw=password so password will be hashed
        # Returns a tuple, where first value is BOOL.
        # If True ok, If False no new user is created
        unique_properties = ['username']
        auth_id = "own:%s" % username
        user = self.auth.store.user_model.create_user(
            auth_id, unique_properties, password_raw=password,
            username=username, company=company.key, ip=self.request.remote_addr
        )

        if not user[0]: #user is a tuple
            if "username" in str(user[1]):
                self.write("username already exists")
                return
            elif "email" in str(user[1]):
                self.write("email exists")
                return
            else:
                self.write("user already register")
                return

        self.write("Done")