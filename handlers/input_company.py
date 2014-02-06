from handler import Handler
import models

import logging

class InputCompanyHandler(Handler):
    def get(self):
        self.render("/html/input-company.html")

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
        tax_id = self.request.get('tax-id')
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

        # Log all form input
        logging.info("UploadCompanyHandler POST Method Logs")
        logging.info("Username: " + username)
        logging.info("Password:" + password)
        logging.info("Company Name: " + name)
        logging.info("Is Buyer: " + str(is_buyer))
        logging.info("Is Supplier: " + str(is_supplier))
        logging.info("Company Address: " + company_address)
        logging.info("Tax ID: " + tax_id)
        logging.info("Company Phone: " + company_phone)
        logging.info("Company Email: " + company_email)
        logging.info("Contact Person:" + contact_person)
        logging.info("Contact Person Phone: " + contact_phone)
        logging.info("Comtact Person Email: " + contact_email)
        
        # Put form input into model and database
        company = models.Company()
        company.username = username
        company.password = password
        company.registered = True
        company.name = name
        company.is_buyer = is_buyer
        company.is_supplier = is_supplier
        company.address = company_address
        company.tax_id = tax_id
        company.company_phone = company_phone
        company.company_email = company_email
        company.contact_person = contact_person
        company.contact_phone = contact_phone
        company.contact_email = contact_email

        company.put()

        self.write("Done")