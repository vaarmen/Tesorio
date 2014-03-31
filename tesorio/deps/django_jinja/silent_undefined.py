#
# author: rattray.alex@gmail.com
#

from jinja2 import Undefined
import logging

class SilentUndefined(Undefined):
    '''
    Dont break pageloads because vars arent there!
    '''
    def _fail_with_undefined_error(self, *args, **kwargs):
        logging.exception('JINJA2: something was undefined!'
            ' (alex is silencing error)')
        return None
