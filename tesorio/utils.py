import logging
from django.utils.html import strip_tags

import sendgrid

import settings
import credentials

sg = sendgrid.SendGridClient(
    credentials.SENDGRID_USER,
    credentials.SENDGRID_PASS
)


if settings.DEBUG:
    from colorlog import ColoredFormatter

    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(asctime)s,"
        "%(msecs)d %(module)s:%(funcName)s:%(lineno)d%(reset)s  "
        "%(white)s%(message)s",
        datefmt='%H:%M:%S',
        reset=True,
        log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
        }
    )
    logger = logging.getLogger()
    if len(logger.handlers) > 1:
        logger.handlers[0].setFormatter(formatter)
        logger.handlers[1].setFormatter(formatter)
    else:
        logger.addHandler(logging.StreamHandler())
        logger.handlers[0].setFormatter(formatter)

logging.getLogger().setLevel(logging.DEBUG)


def email_offer_confirmation(offer):
    offer_params = offer.parameters
    buyer = offer_params.buyer
    supplier = offer_params.supplier
    email_context = locals()  # todo: be less lazy.

    # send to buyer
    text_body = loader.render_to_string('email/buyer_confirm.txt', context)
    context['text_body'] = text_body.replace('\n', '<br>')
    html_body = loader.render_to_string('email/buyer_confirm.jinja', context)
    message = sendgrid.Mail(
        to=buyer.email,
        subject=u'Tesorio | Early payment confirmed to {supplier}'.format(
            supplier=supplier),
        html=html_body,
        text=text_body,
        from_email='Tesorio Confirmation <carlos@tesorio.com>'
    )
    status, msg = sg.send(message)
    logging.debug(safe_format('sent message: {},\n status: {}, msg: {}',
        message, status, msg))

    # send to supplier
    text_body = loader.render_to_string('email/supplier_confirm.txt', context)
    context['text_body'] = text_body.replace('\n', '\n<br>')
    html_body = loader.render_to_string('email/supplier_confirm.jinja', context)
    message = sendgrid.Mail(
        to=supplier.email,
        subject=u'Tesorio | Early payment confirmed from {buyer}'.format(
            buyer=buyer),
        html=html_body,
        text=text_body,
        from_email='Tesorio Confirmation <carlos@tesorio.com>'
    )
    status, msg = sg.send(message)
    logging.debug(safe_format('sent message: {},\n status: {}, msg: {}',
        message, status, msg))

    util.email_admins('Offer Confirmations Sent',
        safe_format('main details: {}', email_context))



def email_admins(subject, body):
    message = sendgrid.Mail(
        to=[u"{0} <{1}>".format(*admin) for admin in settings.ADMINS],
        subject=subject,
        text=body,
        from_email='Tesorio Reporter <noreply@tesorio.com>'
        )
    status, msg = sg.send(message)
    logging.debug(safe_format('message: {},\n status: {}, msg: {}',
        message, status, msg))



def update(instance, **kwargs):
      '''Updates model instance with SQL UPDATE query.
      Useful for updating only certain fields.
      Args:
      instance: eg; prof_alex
      **kwargs: the fields and their values to update
      eg: util.update(prof,
        institution="the streets", department="kicking ass")

    note: returns number of rows affected, not the new model!
    '''
    model = instance.__class__
    return model.objects.filter(id=instance.id).update(**kwargs)


class UnicodePrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)

upprint = UnicodePrettyPrinter()


def upprint_dict(obj):
  ''' Try to safely return unicode of object.
      Incorporates some of the weird-ass fixes and common patterns we've needed.
  '''
  # first, try to get the __dict__ of the item, it's way more fun that way.
  try:
    thing = obj.__dict__
    thing = unicode(upprint.pformat(thing), 'utf-8')
  except:
    thing = obj

  try:
    return unicode(thing)
  except:
    try:
      return str(thing).decode('utf8')
    except:
      return u'<< UNPRINTABLE OBJ >>'


def safe_format(fmt, *args, **kwargs):
  ''' Safe string formatting, with __dict__'s where possible. '''
  try:
    return unicode(fmt).format(*[upprint_dict(obj) for obj in args], **kwargs)
  except:
    try:
      return unicode(fmt).format(*args, **kwargs)
    except:
      try:
        return fmt.format(*[upprint_dict(obj) for obj in args], **kwargs)
      except:
        try:
          return fmt.format(*args, **kwargs)
        except:
          return '<< UNPRINTABLE MESSAGE >>'