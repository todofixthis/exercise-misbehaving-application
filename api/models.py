# coding=utf-8
from __future__ import absolute_import, unicode_literals

from uuid import uuid4

from json_field import JSONField
from django.db import models

from api.value_objects import ApplicantObject


class Session(models.Model):
  session_key = models.UUIDField(primary_key=True, default=uuid4)
  session_data = JSONField()

  @property
  def applicant_vo(self):
    """
    Hydrates applicant data from the session and returns a COPY as a value object.

    IMPORTANT:  you must invoke `applicant_vo.setter` to update the session data.

    :rtype: ApplicantObject
    """
    return ApplicantObject.hydrate(self.session_data.get('applicant') or {})

  @applicant_vo.setter
  def applicant_vo(self, applicant):
    """
    Stores applicant data in the session.

    :type applicant: ApplicantObject
    """
    self.session_data['applicant'] = applicant.dehydrate()