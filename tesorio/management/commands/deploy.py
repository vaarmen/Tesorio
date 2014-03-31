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
    # args = '<poll_id poll_id ...>'
    help = 'This is a script to deploy to gae. Intended usage: ./manage.py deploy'

    def handle(self, *args, **options):

        shell('git commit --allow-empty -m "Deploying to Production at `date`"')

        appcfg_update_cmd = 'appcfg.py update . --oauth2'
        self.stdout.write('-> About to run' + appcfg_update_cmd)
        shell(appcfg_update_cmd)

        self.stdout.write('-> About to migrate prod')
        try:
            # todo: get this from app.yaml
            version_id = '3'
            shell('''
                export SERVER_SOFTWARE='Production';
                export CURRENT_VERSION_ID='{}.local';
                python manage.py syncdb
                python manage.py migrate
            '''.format(version_id)
            )
        finally:
            shell('''
                export CURRENT_VERSION_ID=''
                export SERVER_SOFTWARE='Development'
            ''')