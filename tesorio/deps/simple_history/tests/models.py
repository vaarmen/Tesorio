from __future__ import unicode_literals

from django.db import models
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:  # django 1.4 compatibility
    from django.contrib.auth.models import User

from simple_history.models import HistoricalRecords
from simple_history import register


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    history = HistoricalRecords()


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()

register(Choice)


class Place(models.Model):
    name = models.CharField(max_length=100)


class Restaurant(Place):
    rating = models.IntegerField()

    updates = HistoricalRecords()


class Person(models.Model):
    name = models.CharField(max_length=100)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if hasattr(self, 'skip_history_when_saving'):
            raise RuntimeError('error while saving')
        else:
            super(Person, self).save(*args, **kwargs)


class FileModel(models.Model):
    file = models.FileField(upload_to='files')
    history = HistoricalRecords()


class Document(models.Model):
    changed_by = models.ForeignKey(User, null=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by


register(User, app='simple_history.tests', manager_name='histories')


class ExternalModel1(models.Model):
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    class Meta:
        app_label = 'external'

class ExternalModel3(models.Model):
    name = models.CharField(max_length=100)

register(ExternalModel3, app='simple_history.tests.external',
    manager_name='histories')
