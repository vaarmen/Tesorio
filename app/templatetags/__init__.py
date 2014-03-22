# from https://github.com/niwibe/django-jinja/blob/master/docs/differences.rst
# <someapp>/templatetags/<anyfile>.py
from django_jinja import library

lib = library.Library()

@lib.global_function
def format_currency(value):
    return "${:,.2f}".format(float(value))