#!/usr/bin/env python
#
# Author: Alex Rattray (rattray.alex@gmail.com)
import sys
import subprocess
from django.core.management.base import BaseCommand, CommandError

# yells at you otherwise, has to do with connecting to google cloud sql
# (If you need to connect directly to the google cloud sql,
# use the google_sql.py script, which should be on your path.)
sys.path.insert(0, '/usr/local/google_appengine/')

def shell(cmd, *args, **kwargs):
  return subprocess.call(cmd, shell=True, *args, **kwargs)


class Command(BaseCommand):
    # options = ['--nodebug',]
    # args = '<--nodebug, >'

    def handle(self, *args, **options):
        self.stdout.write('-> Running devekopment server.')
        # if '--nodebug' in sys.argv:
        #     shell('dev_appserver.py .')
        # else:
        shell('dev_appserver.py . --log_level=debug')
