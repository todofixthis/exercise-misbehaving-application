# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from django.views.generic import View

from api.forms import ApplicantForm


class Applicant(View):
  @staticmethod
  def get(request):
    return render(request, 'applicant.html', {
      'form':       ApplicantForm,
      'applicant':  request.session.get_applicant_vo(),
    })

  @staticmethod
  def post(request):
    form = ApplicantForm(request.POST)

    if form.is_valid():
      request.session.update_applicant_vo(form.cleaned_data)

    return render(request, 'applicant.html', {
      'form':       form,
      'applicant':  request.session.get_applicant_vo(),
    })