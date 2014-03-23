# Create your views here.
import urlparse
from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# django views
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

# model imports
from models import Invoice, OfferParameters


class TesorioTemplateView(TemplateView):
    def render(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(TesorioTemplateView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['company_name'] = self.request.user.person.company.name if self.request.user.is_authenticated() else None
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


class HomeDashboard(TesorioTemplateView):
    template_name = 'home_dashboard.jinja'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeDashboard, self).dispatch(*args, **kwargs)

    def not_registered(self, request, *args, **kwargs):
        self.template_name = 'registration.jinja'
        return self.render()

    def get(self, request, *args, **kwargs):
        user = request.user
        person = user.person
        company = person.company

        if not company.has_registered:
            return self.not_registered(request, *args, **kwargs)

        return self.render(
            company=company,
        )


class BuyerDashboard(TesorioTemplateView):
    template_name = 'buyer_dashboard.jinja'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BuyerDashboard, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # messages.info(request, 'hi fabio')
        user = request.user
        person = user.person
        company = person.company
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
        invoices = company.supplier_invoices.all()
        return self.render(
            company=company,
            invoices=invoices,
        )


class InvoiceView(DetailView):
    template_name = "invoice.jinja"
    model = Invoice

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InvoiceView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(InvoiceView, self).get_context_data(**kwargs)

        invoice = self.object
        parameters = OfferParameters.objects.get(
            buyer=invoice.buyer,
            supplier=invoice.supplier)
        user = self.request.user

        context['invoice'] = invoice
        context['parameters'] = parameters

        company = user.person.company

        if invoice.buyer == company:
            context['buyer'] = True
        elif invoice.supplier == company:
            context['supplier'] = True
        else:
            context['invalid'] = True

        return contex