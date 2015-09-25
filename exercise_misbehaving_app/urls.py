# coding=utf-8
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from api.views import Applicant

urlpatterns = [
    url(r'^applicant$', Applicant.as_view(), name='applicant')
]
