import logging
from django import forms
from app.models import (
  Company,
)


class RegistrationForm(forms.ModelForm):
    # todo: test that django does, indeed, work server-side ;-P
    accept_tos = forms.BooleanField(
        required=True,
        label="I accept the Terms of Service."
    )
    class Meta:
        model = Company
        fields = [
            'name',
            'ein',
            'address',
            'phone',
            'email',
        ]