# coding=utf-8
from __future__ import absolute_import, unicode_literals

from uuid import uuid4

from django.contrib.sessions.backends.base import CreateError
from django.contrib.sessions.backends.db import SessionStore as DjangoSessionStore
from django.db import router, IntegrityError
from django.db.transaction import savepoint, savepoint_rollback, savepoint_commit

from api.models import Session
from api.value_objects import ApplicantObject


class SessionStore(DjangoSessionStore):
    """
    Database-backed sessions using custom API model.
    """
    # Key differences between Django sessions and our sessions:
    #   - Different DB table.
    #   - Session data is a JSONField.
    #   - No expiration.
    session_class = Session

    def __init__(self, session_key=None):
        super(SessionStore, self).__init__(session_key)

        # We check whether the session exists quite often, so we'll cache it locally to minimize DB lookups.
        self._exists = None
        """:type: bool"""

    def get_applicant_vo(self):
        """
        Returns a value object representation of the applicant.

        IMPORTANT:  Modifications made to this object will NOT be persisted in the session; you must call
            `set_applicant_vo` before calling `save`!

        :rtype: ApplicantObject
        """
        return ApplicantObject.hydrate(self.get('applicant') or {})

    def set_applicant_vo(self, applicant):
        """
        Stores applicant values in the session.

        :type applicant: ApplicantObject
        """
        self['applicant'] = applicant.dehydrate()

    def update_applicant_vo(self, applicant):
        """
        Hydrates the ApplicantObject stored in the session, updates its attributes from another ApplicantObject and
            stores the modified values back in the session.

        :type applicant: ApplicantObject
        """
        existing = self.get_applicant_vo()
        existing.update(applicant)
        self.set_applicant_vo(existing)

    def load(self):
        try:
            session_obj = self.session_class.objects.get(session_key=self.session_key)
        except self.session_class.DoesNotExist:
            self._exists = False
            return {}
        else:
            self._exists = True
            return session_obj.session_data

    def exists(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return None

            session_key = self._session_key

        if session_key == self._session_key:
            if self._exists is None:
                self._exists = self._check_exists(session_key)
            return self._exists
        else:
            return self._check_exists(session_key)

    def save(self, must_create=False):
        obj = self.session_class(
            session_data        = self._get_session(no_load=must_create),
            session_key         = self._get_or_create_session_key(),
        )

        using   = router.db_for_write(self.session_class, instance=obj)
        sid     = savepoint(using=using)

        try:
            obj.save(force_insert=must_create, using=using)
        except IntegrityError:
            savepoint_rollback(sid, using=using)

            if must_create:
                raise CreateError()
            raise
        else:
            savepoint_commit(sid, using=using)

            self._exists    = True
            self.accessed   = True
            self.modified   = False

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return

            session_key = self._session_key

        self.session_class.objects.filter(session_key=session_key).delete()

        if session_key == self._session_key:
            self._exists = False

    def _get_new_session_key(self):
        return uuid4().hex

    def _check_exists(self, session_key):
        """
        Pings the database to see if a given session key exists.

        This method is intended to be called internally; use `exists` instead.

        :type session_key: unicode

        :rtype: bool
        """
        return self.session_class.objects.filter(session_key=session_key).count() > 0