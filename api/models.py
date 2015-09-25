# coding=utf-8
from __future__ import absolute_import, unicode_literals

from json_field import JSONField

from django.db import models


class Session(models.Model):
  session_key = models.UUIDField(primary_key=True)
  session_data = JSONField()