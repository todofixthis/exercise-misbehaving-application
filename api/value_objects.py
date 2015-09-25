# coding=utf-8
from __future__ import absolute_import, unicode_literals

from api.value_object import fields
from api.value_object.base import BaseValueObject


class ApplicantObject(BaseValueObject):
  first_name  = fields.Primitive()
  last_name   = fields.Primitive()
  gender      = fields.Primitive()
  # birthday    = fields.Date()
  email       = fields.Primitive()