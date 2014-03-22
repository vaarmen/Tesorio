from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# import views
from app import views

# from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tesorio.views.home', name='home'),
    # url(r'^tesorio/', include('tesorio.foo.urls')),

    url(r'^$', views.IndexView.as_view(), name='home'),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
