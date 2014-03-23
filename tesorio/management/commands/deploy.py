#!/usr/bin/env python
#
# Author: Alex Rattray (rattray.alex@gmail.com)
import subprocess

print 'This is a script to deploy to gae'
print 'intended usage: ./manage.py deploy'


def shell(cmd, *args, **kwargs):
  return subprocess.call(cmd, shell=True, *args, **kwargs)


shell('git commit --allow-empty -m "Deploying to Production at `date`"')

appcfg_update_cmd = 'appcfg.py update . --oauth2'
print '-> About to run', appcfg_update_cmd
shell(appcfg_update_cmd)

print '-> About to migrate prod'
try:
    version_id = '2'
    shell('''
        export SERVER_SOFTWARE='Production';
        export CURRENT_VERSION_ID='{}.local'
        python manage.py syncdb
        python manage.py migrate
    '''.format(version_id)
    )
finally:
    shell('''
        export CURRENT_VERSION_ID=''
        export SERVER_SOFTWARE='Development'
    ''')