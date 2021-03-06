import logging
import pprint
from django.utils.html import strip_tags
from django.template import loader

import sendgrid

import settings
import credentials

# python libs
from datetime import date, timedelta

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

def calculate_discount(amount, discount):
    return (100 - discount)/100 * amount

def calculate_date(date, days):
    return date - timedelta(days=days)

def calculate_profit(original_amount, discount_amount):
    return original_amount - discount_amount

def calculate_apr(discount, days_accelerated):
    return discount
    # return (365 / days_accelerated) * discount

def invalid_offer_date(date):
    # https://github.com/FabioFleitas/Tesorio/issues/2
    return date.today() >= date

def valid_offer(invoice, offer_params, option, percent, days_acc):
    # verify arguments
    if not invoice or not offer_params or not option or not percent or not days_acc:
        return False

    if option == '1':
        percent_check = offer_params.alt_1_percent
        days_acc_check = offer_params.alt_1_days
    elif option == '2':
        percent_check = offer_params.alt_2_percent
        days_acc_check = offer_params.alt_2_days
    elif option == '3':
        percent_check = offer_params.alt_3_percent
        days_acc_check = offer_params.alt_3_days
    else:
        return False

    # verify arguments to offer_params
    if not percent == unicode(percent_check) or not days_acc == unicode(days_acc_check):
        return False

    # verify invalid_offer_date
    date = calculate_date(invoice.due_date, days_acc_check)
    if invalid_offer_date(date):
        return False

    ## verify apr

    return True

def email_offer_confirmation(offer):
    offer_params = offer.parameters
    buyer = offer_params.buyer
    supplier = offer_params.supplier
    context = locals()  # todo: be less lazy.

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
        from_email='carlos@tesorio.com'
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
        from_email='carlos@tesorio.com'
    )
    status, msg = sg.send(message)
    logging.debug(safe_format('sent message: {},\n status: {}, msg: {}',
        message, status, msg))

    email_admins('Offer Confirmations Sent',
        safe_format('main details: {}', context))
    return


def email_admins(subject, body):
    message = sendgrid.Mail(
        to=[admin[1] for admin in settings.ADMINS],
        subject=subject,
        text=body,
        from_email='noreply@tesorio.com'
        )
    status, msg = sg.send(message)
    logging.debug(safe_format('mailed admins: \n\n message: {},\n status: {}, msg: {}',
        message, status, msg))

def email_file(upload, company_name):
    message = sendgrid.Mail(
        to=[admin[1] for admin in settings.ADMINS],
        subject=company_name + " file upload",
        text="See attachment",
        from_email='noreply@tesorio.com'
        )

    message.add_attachment_stream(upload.name, upload.file.getvalue())
    status, msg = sg.send(message)
    logging.debug(safe_format('mailed admins: \n\n message: {},\n status: {}, msg: {}',
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