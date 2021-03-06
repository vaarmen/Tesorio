# from https://github.com/niwibe/django-jinja/blob/master/docs/differences.rst
# <someapp>/templatetags/<anyfile>.py
from django_jinja import library
lib = library.Library()

# python libs
from datetime import timedelta, date

import utils

@lib.global_function
def calculate_discount(amount, discount):
    return utils.calculate_discount(amount, discount)

@lib.global_function
def calculate_date(date, days):
    return utils.calculate_date(date, days)

@lib.filter
def format_currency(value):
    return "${:,.2f}".format(float(value))

@lib.filter
def format_date(date):
    return date.strftime('%m-%d-%Y')

@lib.filter
def format_date_formal(date):
    return date.strftime('%A, %B %d, %Y')

@lib.global_function
def invalid_offer_date(date):
	# https://github.com/FabioFleitas/Tesorio/issues/2
	return utils.invalid_offer_date(date)