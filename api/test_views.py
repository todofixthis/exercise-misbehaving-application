# coding=utf-8
from __future__ import absolute_import, unicode_literals

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
      self.assertEqual(applicant.email, 'marcus.brody@marshall.edu')

  def test_update_applicant(self):
      """
      Update an existing applicant.
      """
      self.client.session.update_applicant_vo(ApplicantObject({
        'first_name': 'Marcus',
        'last_name':  'Brody',
        'gender':     'm',
        'email':      'marcus.brody@marshall.edu',
      }))

      response = self.client.post(reverse('applicant'), {
        'first_name': 'Marion',
        'last_name':  'Ravenwood',
        'gender':     'f',
        'email':      'marion@ravens-nest.com',
      })
      """:type: django.http.HttpResponse"""
      self.assertEqual(response.status_code, 200)

      # Applicant details are updated in the session.
      applicant = self.client.session.get_applicant_vo()

      self.assertIsInstance(applicant, ApplicantObject)

      self.assertEqual(applicant.first_name, 'Marion')
      self.assertEqual(applicant.last_name, 'Ravenwood')
      self.assertEqual(applicant.gender, 'f')
      self.assertEqual(applicant.email, 'marion@ravens-nest.com')