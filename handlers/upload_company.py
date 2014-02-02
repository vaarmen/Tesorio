from handler import Handler
import models

class UploadCompanyHandler(Handler):
    def get(self):
        self.render("/html/upload-company.html")

    def post(self):
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

        # Convert to bool
        if is_buyer: is_buyer = True
        else: is_buyer = False

        if is_supplier: is_supplier = True
        else: is_supplier = False

        company_address = address + ", " + city + ", " + state + ", " + zip_code
        
        company = models.Company()
        company.username = username
        company.password = password
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