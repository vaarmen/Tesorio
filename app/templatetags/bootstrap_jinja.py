from django_jinja import library
from bootstrap3.forms import render_form
from django.template.loader import get_template
from django.template import RequestContext
lib = library.Library()


message_fields = {
    'debug': {
        'title': 'Debug!',
        'icon': 'fa fa-check',
        'color': '#739E73'
    },
    'info': {
        'title': 'Notification!',
        'icon': 'fa fa-bell swing animated',
        'color': '#296191'
    },
    'success': {
        'title': 'Success!',
        'icon': 'fa fa-check',
        'color': '#739E73'
    },
    'warning': {
        'title': 'Warning!',
        'icon': 'fa fa-shield fadeInLeft animated',
        'color': '#C79121'
    },
    'error': {
        'title': 'Success!',
        'icon': 'fa fa-warning shake animated',
        'color': '#C46A69'
    },
}

@lib.global_function
def bootstrap_form(*args, **kwargs):
  return render_form(*args, **kwargs)

@lib.global_function
def bootstrap_messages(request, messages, *args, **kwargs):
  context = RequestContext(request, {'messages': messages})
  return get_template(
    'bootstrap3/messages.html'
  ).render(context)

@lib.global_function
def get_message_title():
  return 'lol'
  # return message_fields[message_tags]['title']

@lib.global_function
def message_icon(message_tags):
  return message_fields[message_tags]['icon']

@lib.global_function
def message_color(message_tags):
  return message_fields[message_tags]['color']