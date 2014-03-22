#!/usr/bin/env python
import subprocess

print 'run from Tesorio/tesorio/, eg tesorio/scripts/nuke_db.py'

def shell(cmd, *args, **kwargs):
  return subprocess.check_call(cmd, shell=True, *args, **kwargs)

shell('mysql -u root -p < tesorio/scripts/recreate_db.sql')

# shell('rm app/migrations/*')
# shell('touch tesorio/migrations/__init__.py')

shell('./manage.py syncdb')

# shell('./manage.py schemamigration app --initial')
# dont need to for longerusername

shell('./manage.py migrate')