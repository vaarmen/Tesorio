# Create your views here.
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied

# django views
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.detail import DetailView

# tesorio imports
import forms
import utils
from models import (
    Invoice,
    Company,
    OfferParameters,
    Offer
)

# stdlib
import logging
import urlparse


class CompanyNotRegistered(PermissionDenied):
    pass


def check_company_registered(company):
    if not company.has_registered:
        raise CompanyNotRegistered()


class TesorioTemplateView(TemplateView):

    def render(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(TesorioTemplateView, self).get_context_data(**kwargs)
        context['request'] = self.request

        if self.request.user.is_authenticated():
            user = self.request.user
            person = user.person
            context['company'] = person.company
            context['person_name'] = user.first_name + "." + user.last_name

        return context


class IndexView(TesorioTemplateView):
    template_name = "index.jinja"


    def get(self, request, *args, **kwargs):
        return self.render()


class LoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.
    from https://gist.github.com/stefanfoulis/1140136

    Usage:
        in urls.py:
            url(r'^login/$',
                AuthenticationView.as_view(
                    form_class=MyCustomAuthFormClass,
                    success_url='/my/custom/success/url/),
                name="login"),

    """
    form_class = AuthenticationForm
    redirect_field_name = auth.REDIRECT_FIELD_NAME
    template_name = 'login.jinja'
    success_url = '/dashboard/'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log him in.
        """
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        redirect_to = self.request.GET.get('next') or self.success_url

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect('/')


class RegistrationView(UpdateView):
    template_name = 'registration.jinja'
    form_class = forms.RegistrationForm
    success_url = '/dashboard/'
    redirect_field_name = auth.REDIRECT_FIELD_NAME

    def get_object(self):
        user = self.request.user
        person = user.person
        company = person.company
        return company

    def get_success_url(self):
        redirect_to = self.request.GET.get('next') or self.success_url

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def form_valid(self, form):
        # update has_registered on company to True
        company = self.get_object()
        company.has_registered = True
        company.save()

        return super(RegistrationView, self).form_valid(form)

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(RegistrationView, self).dispatch(*args, **kwargs)


class HomeDashboard(TesorioTemplateView):
    template_name = 'home_dashboard.jinja'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeDashboard, self).dispatch(*args, **kwargs)

    def not_registered(self, request, *args, **kwargs):
        self.template_name = 'registration.jinja'
        return self.render()

    def get(self, request, *args, **kwargs):
        # messages.info(request, 'Hello there!')

        user = request.user
        person = user.person
        company = person.company

        try: check_company_registered(company)
        except: return HttpResponseRedirect('/registration/')

        return self.render(
            company=company,
        )


class BuyerDashboard(TesorioTemplateView):
    template_name = 'buyer_dashboard.jinja'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuyerDashboard, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        person = user.person
        company = person.company

        try: check_company_registered(company)
        except: return HttpResponseRedirect('/registration/')

        invoices = company.buyer_invoices.all()
        return self.render(
            company=company,
            invoices=invoices,
        )


class SupplierDashboard(TesorioTemplateView):
    template_name = 'supplier_dashboard.jinja'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SupplierDashboard, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = request.user
        person = user.person
        company = person.company

        try: check_company_registered(company)
        except: return HttpResponseRedirect('/registration/')

        invoices = company.supplier_invoices.all()
        return self.render(
            company=company,
            invoices=invoices,
        )


class InvoiceView(TesorioTemplateView):
    template_name = 'invoice.jinja'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InvoiceView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        invoice_id = kwargs['pk']
        invoice = Invoice.objects.get(
            pk=invoice_id
        )
        parameters = OfferParameters.objects.get(
            buyer=invoice.buyer,
            supplier=invoice.supplier)
        user = self.request.user

        option = request.GET.get('option')

        context = {}

        context['invoice'] = invoice
        context['parameters'] = parameters
        context['option'] = option

        company = user.person.company

        if invoice.buyer == company:
            context['buyer'] = True
        elif invoice.supplier == company:
            context['supplier'] = True
        else:
            context['invalid'] = True
            return HttpResponseRedirect('/dashboard/') ## change later

        return self.render(**context)

    def post(self, request, *args, **kwargs):
        invoice_id = kwargs['pk']
        invoice = Invoice.objects.get(
            pk=invoice_id
        )
        parameters = OfferParameters.objects.get(
            buyer=invoice.buyer,
            supplier=invoice.supplier)
        user = self.request.user

        context = {}

        context['invoice'] = invoice
        context['parameters'] = parameters

        company = user.person.company

        if invoice.buyer == company:
            context['buyer'] = True
        elif invoice.supplier == company:
            context['supplier'] = True
        else:
            context['invalid'] = True
            return HttpResponseRedirect('/dashboard/') ## change later

        # POST data
        option = request.POST.get('option')
        percent = request.POST.get('percent')
        days_acc = request.POST.get('days-acc')

        if utils.valid_offer(invoice, parameters, option, percent, days_acc):
            messages.info(request, "Good offer")

            # fix this later
            if option == '1':
                percent_param = parameters.alt_1_percent
                days_acc_param = parameters.alt_1_days
            elif option == '2':
                percent_param = parameters.alt_2_percent
                days_acc_param = parameters.alt_2_days
            elif option == '3':
                percent_param = parameters.alt_3_percent
                days_acc_param = parameters.alt_3_days

            discount_amount = utils.calculate_discount(invoice.amount, percent_param)

            # create new offer model object
            offer = Offer()
            offer.invoice = invoice
            offer.parameters = parameters
            offer.discount = percent_param
            offer.days_accelerated = days_acc_param
            offer.date_due = utils.calculate_date(invoice.due_date, days_acc_param)
            offer.amount = discount_amount
            offer.status = 'CLEARED'
            offer.profit = utils.calculate_profit(invoice.amount, discount_amount)
            offer.apr = utils.calculate_apr(percent_param, days_acc_param)
            offer.save()

            invoice.current_bid = offer
            invoice.status = 'CLEARED'
            invoice.save()

            ## fix this
            # utils.email_offer_confirmation(offer)

            ### need to send messages to respective parties
            ### perhaps have in Offer field
            ### the Person who did the offer


        else:
            messages.error(request, "Bad offer")


        return self.render(**context)

class UploadView(TesorioTemplateView):
    template_name = 'upload.jinja'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render()

    def post(self, request, *args, **kwargs):
        upload_file = request.FILES['file']
        company_name = request.user.person.company.name

        utils.email_file(upload_file, company_name)

        return HttpResponse()

# class InvoiceViewOld(DetailView):
#     template_name = "invoice.jinja"
#     model = Invoice

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(InvoiceView, self).dispatch(*args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(InvoiceView, self).get_context_data(**kwargs)

#         # base context (could not inherit from TesorioTemplateView)
#         context['request'] = self.request

#         if self.request.user.is_authenticated():
#             user = self.request.user
#             person = user.person
#             context['company_name'] = person.company
#             context['person_name'] = user.first_name + "." + user.last_name
#         # end base

#         invoice = self.object
#         parameters = OfferParameters.objects.get(
#             buyer=invoice.buyer,
#             supplier=invoice.supplier)
#         user = self.request.user

#         context['invoice'] = invoice
#         context['parameters'] = parameters

#         company = user.person.company

#         if invoice.buyer == company:
#             context['buyer'] = True
#         elif invoice.supplier == company:
#             context['supplier'] = True
#         else:
#             context['invalid'] = True

#         return context
