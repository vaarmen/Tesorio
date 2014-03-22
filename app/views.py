# Create your views here.
import urlparse
from django.views.generic import TemplateView, View
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView


class TesorioTemplateView(TemplateView):
    def render(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(TesorioTemplateView, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class IndexView(TesorioTemplateView):
    template_name = "index.jinja"

    def get(self, request, *args, **kwargs):
        return self.render()

# class LoginView(TesorioTemplateView):
#     template_name = 'login.jinja'

#     def get(self, request, *args, **kwargs):
#         return self.render()

#     def get(self, request, *args, **kwargs):
#         return self.render()

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
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

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

# class Searc hPageView(FormView):
#     template_name = 'search/search.html'

#     def get(self, request, *args, **kwargs):
#         self.bookmarks = []
#         self.show_results = False
#         form = SearchForm(self.request.GET or None)
#         if form.is_valid():
#             self.show_results = True
#             self.bookmarks = Bookmark.objects.filter(title__icontains=form.cleaned_data['query'])[:10]

#         return self.render_to_response(self.get_context_data(form=form))


#     def get_context_data(self, **kwargs):
#         context = super(SearchPageView, self).get_context_data(**kwargs)
#         context.update({
#             'show_tags': True,
#             'show_user': True,
#             'show_results': self.show_results,
#             'bookmarks': self.bookmarks
#         })
#         return context