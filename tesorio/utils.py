import logging

import settings


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
