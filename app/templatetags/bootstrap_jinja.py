from django_jinja import library
from bootstrap3.forms import render_form
from django.template.loader import get_template
from django.template import RequestContext
lib = library.Library()


@lib.global_function
def bootstrap_form(*args, **kwargs):
  return render_form(*args, **kwargs)

@lib.global_function
def bootstrap_messages(request, messages, *args, **kwargs):
  context = RequestContext(request, {'messages': messages})
  return get_template(
    'bootstrap3/messages.html'
  ).render(context)