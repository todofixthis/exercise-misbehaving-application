# coding=utf-8
from __future__ import absolute_import, unicode_literals

from datetime import date

from django.core.urlresolvers import reverse
from django.test import TestCase

from api.value_objects import ApplicantObject


class ApplicantTestCase(TestCase):
  def test_create_applicant(self):
      """
      Create a new applicant.
      """
      response = self.client.post(reverse('applicant'), {
        'first_name': 'Marcus',
        'last_name':  'Brody',
        'gender':     'm',
        # :kludge: Marcus Brody was actually born in 1878, but we have to use year >= 1900.
        # :see: http://stackoverflow.com/a/1644026
        'birthday':   '1900-08-13',
        'email':      'marcus.brody@marshall.edu',
      })
      """:type: django.http.HttpResponse"""
      self.assertEqual(response.status_code, 200)

      # Applicant details are now stored in the session.
      applicant = self.client.session.get_applicant_vo()

      self.assertIsInstance(applicant, ApplicantObject)

      self.assertEqual(applicant.first_name, 'Marcus')
      self.assertEqual(applicant.last_name, 'Brody')
      self.assertEqual(applicant.gender, 'm')
      self.assertEqual(applicant.birthday, date(1900, 8, 13))
      self.assertEqual(applicant.email, 'marcus.brody@marshall.edu')

  def test_update_applicant(self):
      """
      Update an existing applicant.
      """
      self.client.session.update_applicant_vo(ApplicantObject({
        'first_name': 'Marcus',
        'last_name':  'Brody',
        'gender':     'm',
        'birthday':   date(1900, 8, 13),
        'email':      'marcus.brody@marshall.edu',
      }))

      response = self.client.post(reverse('applicant'), {
        'first_name': 'Marion',
        'last_name':  'Ravenwood',
        'gender':     'f',
        'birthday':   '1909-03-23',
        'email':      'mravenwood1@aol.com',
      })
      """:type: django.http.HttpResponse"""
      self.assertEqual(response.status_code, 200)

      # Applicant details are updated in the session.
      applicant = self.client.session.get_applicant_vo()

      self.assertIsInstance(applicant, ApplicantObject)

      self.assertEqual(applicant.first_name, 'Marion')
      self.assertEqual(applicant.last_name, 'Ravenwood')
      self.assertEqual(applicant.gender, 'f')
      self.assertEqual(applicant.birthday, date(1909, 3, 23))
      self.assertEqual(applicant.email, 'mravenwood1@aol.com')
