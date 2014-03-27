import logging
from django import forms
from app.models import (
  Company,
)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'ein',
            'address',
            'phone',
            'email',
            # 'email',

        ]