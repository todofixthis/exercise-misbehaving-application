# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django import forms

from api.value_objects import ApplicantObject


class ApplicantForm(forms.Form):
  first_name  = forms.CharField()
  last_name   = forms.CharField()
  gender      = forms.ChoiceField(choices=(('m', 'Male'), ('f', 'Female')))
  birthday    = forms.DateField(label='Birthday (YYYY-MM-DD)')
  email       = forms.CharField()

  def clean(self):
    return ApplicantObject(self.cleaned_data)
