#!/usr/bin/env python
import sys
import subprocess
from django.core.management.base import BaseCommand, CommandError

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
