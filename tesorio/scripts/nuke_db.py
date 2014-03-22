#!/usr/bin/env python
import subprocess

print 'run from Tesorio/tesorio/, eg tesorio/scripts/nuke_db.py'

def shell(cmd, *args, **kwargs):
  return subprocess.check_call(cmd, shell=True, *args, **kwargs)

shell('mysql -u root -p < tesorio/scripts/recreate_db.sql')

# clears/resets the migrations folder (for *totally* starting from scratch)
# shell('rm app/migrations/*')
# shell('touch app/migrations/__init__.py')

shell('./manage.py syncdb')

# again, only need if you're *totally* starting from scratch.
# shell('./manage.py schemamigration app --initial')

shell('./manage.py migrate')