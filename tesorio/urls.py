from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# import views
from app import views

import django_jinja.views

handler403 = django_jinja.views.PermissionDenied.as_view()
handler404 = django_jinja.views.PageNotFound.as_view()
handler500 = django_jinja.views.ServerError.as_view()

# from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tesorio.views.home', name='home'),
    # url(r'^tesorio/', include('tesorio.foo.urls')),

    url(r'^$',
        views.IndexView.as_view(),
        name='home'
    ),
    url(r'^login/$',
        views.LoginView.as_view(),
        name="login"
    ),
    url(r'^logout/$',
        views.LogoutView.as_view(),
        name="logout"
    ),
    # this is only used for url-reversing, and must follow the other logout
    url(r'^logout/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'
    ),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/logout/'}
    ),
    url(r'^password/reset/',
        'django.contrib.auth.views.password_reset',
        name='password_reset'
    ),


    url(r'^registration/$',
        views.RegistrationView.as_view(),
        name="registration"
    ),
    url(r'^dashboard/$',
        views.HomeDashboard.as_view(),
        name="home_dashboard"
    ),
    url(r'^dashboard/buyer/$',
        views.BuyerDashboard.as_view(),
        name="buyer_dashboard"
    ),
    url(r'^dashboard/supplier/$',
        views.SupplierDashboard.as_view(),
        name="supplier_dashboard"
    ),
    url(r'^dashboard/invoice/(?P<pk>\d+)/$',
        views.InvoiceView.as_view(),
        name='invoice'
    ),


    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
