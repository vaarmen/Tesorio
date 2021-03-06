from django.db.models import get_models, get_app
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.admin.sites import AlreadyRegistered

from simple_history.admin import SimpleHistoryAdmin

from app.models import *

def autoregister(app_name):
  app_models = get_app(app_name)
  for model in get_models(app_models):
    try:
      if hasattr(model, 'history'):
        admin.site.register(model, SimpleHistoryAdmin)
      elif not u'Historical' in unicode(model):
        admin.site.register(model)
    except AlreadyRegistered:
      pass

autoregister('app')