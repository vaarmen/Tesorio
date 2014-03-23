# from https://github.com/niwibe/django-jinja/blob/master/docs/differences.rst
# <someapp>/templatetags/<anyfile>.py
from django_jinja import library
lib = library.Library()

# python libs
from datetime import timedelta

@lib.global_function
def calculate_discount(amount, discount):
    return (100 - discount)/100 * amount

@lib.global_function
def calculate_date(date, days):
    return date - timedelta(days=days)

@lib.filter
def format_currency(value):
    return "${:,.2f}".format(float(value))

@lib.filter
def format_date(date):
    return date.strftime('%m-%d-%Y')

@lib.filter
def format_date_formal(date):
    return date.strftime('%A, %B %d, %Y')
