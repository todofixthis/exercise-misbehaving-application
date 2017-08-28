# coding=utf-8
from __future__ import absolute_import, unicode_literals

from abc import ABCMeta
from collections import Container
from datetime import datetime
from decimal import Decimal as DecimalType

from pytz import utc
from six import with_metaclass


class Field(with_metaclass(ABCMeta)):
    """
    Base functionality for value object fields.
    """
    def __init__(self, key=None, public=True):
        """
        :type key: unicode
        :param key: The alternate key to use for the field when extracting values from incoming dicts.
            This is useful when you want to use snake_case for Python attribute names, but camelCase for dict keys.

        :type public: bool
        :param public: Whether this value should be included when generating "public" versions of value objects.

        :see: applicant_journey.value_object.base.BaseValueObject#get_public_value
        """
        super(Field, self).__init__()

        self.key    = key
        self.public = public

    def init(self, value):
        """
        Adjusts the incoming value for the field when initializing the parent value object.

        :see: applicant_journey.value_object.base.BaseValueObject#__init__
        """
        return value

    def merge(self, existing, incoming):
        """
        Returns the value that should be used for the field when updating the parent value object from another one.

        :see: applicant_journey.value_object.base.BaseValueObject#update
        """
        return existing if incoming is None else incoming

    def hydrate(self, value):
        """
        Returns the hydrated form of a field's dehydrated value.

        :see: applicant_journey.value_object.base.ValueObjectMeta#hydrate
        """
        return value

    def dehydrate(self, value):
        """
        Returns the dehydrated form of a field value.

        :see: applicant_journey.value_object.base.BaseValueObject#dehydrate
        """
        return value

    def make_public_value(self, value):
        """
        Returns the "public" version of a field value.

        :see: applicant_journey.value_object.base.BaseValueObject#get_public_value
        """
        return self.dehydrate(value)


class Primitive(Field):
    """
    Stores a primitive value, i.e., one that can be safely serialized and unserialized without any modification.

    Examples of primitive types include:

        - unicode (but NOT str; use Bytes field for those!)
        - int
        - float

    Examples of non-primitive types include:

        - dict (use Collection field)
        - datetime.datetime (use Datetime field)
        - decimal.Decimal (use Decimal field)
        etc.
    """
    pass


class Collection(Field):
    """
    A field that contains a collection of other fields of the same type.
    """
    def __init__(self, sub_field=Primitive, key=None, public=True):
        """
        :type sub_field: Union[Field, () -> Field, applicant_journey.value_object.base.ValueObjectMeta]
        :param sub_field: The type of field in this collection.
            Tip:  You can pass a value object class here to configure a collection of value objects.
            Example:
                addresses = fields.Collection(AddressObject)

        :type key: unicode
        :param key: The alternate key to use for the field when extracting values from incoming dicts.
            This is useful when you want to use snake_case for Python attribute names, but camelCase for dict keys.

        :type public: bool|collections.Container[basestring]
        :param public: Depends on type:
            - bool:         Whether this value should be included when generating "public" versions of value objects.
            - Container:    Only these keys should be included in the public version of the value.

        :see: applicant_journey.value_object.base.BaseValueObject#get_public_value
        """
        super(Collection, self).__init__(key, set(public) if isinstance(public, Container) else bool(public))

        from api.value_object.base import ValueObjectMeta

        if isinstance(sub_field, ValueObjectMeta):
            self.sub_field = ValueObject(sub_field)

        elif callable(sub_field):
            self.sub_field = sub_field()

        else:
            self.sub_field = sub_field

    def init(self, value):
        """
        :type value: dict
        """
        if value is None:
            return {}

        return {
            k: self.sub_field.init(v)
                for k, v in value.items()
        }

    def merge(self, existing, incoming):
        merged = {}

        if existing is not None:
            merged.update(existing)

        if incoming is not None:
            merged.update({
                k: self.sub_field.merge(merged.get(k, None), v)
                    for k, v in incoming.items()
            })

        return merged

    def hydrate(self, value):
        """
        :type value: dict
        """
        if value is None:
            return {}

        return {
            k: self.sub_field.hydrate(v)
                for k, v in value.items()
        }

    def dehydrate(self, value):
        """
        :type value: dict
        """
        if value is None:
            return {}

        return {
            k: self.sub_field.dehydrate(v)
                for k, v in value.items()
        }

    def make_public_value(self, value):
        """
        :type value: dict
        """
        if value is None:
            return {}

        fields = set(self.public if isinstance(self.public, set) else value.keys())

        return {
            k: self.sub_field.make_public_value(v)
                for k, v in value.items()
                if k in fields
        }


class ValueObject(Field):
    """
    A field that contains another value object.
    """
    def __init__(self, vo_type, key=None, public=True):
        """
        :type vo_type: applicant_journey.value_object.base.ValueObjectMeta

        :type key: unicode
        :param key: The alternate key to use for the field when extracting values from incoming dicts.
            This is useful when you want to use snake_case for Python attribute names, but camelCase for dict keys.

        :type public: bool|collections.Container[basestring]
        :param public: Depends on type:
            - bool:         Whether this value should be included when generating "public" versions of value objects.
            - Container:    Only these sub-fields should be included in the public version of the value.

        :see: applicant_journey.value_object.base.BaseValueObject#get_public_value
        """
        super(ValueObject, self).__init__(key, set(public) if isinstance(public, Container) else bool(public))

        self.vo_type = vo_type

    def init(self, value):
        """
        Creates a new value object from a dict of values.

        :type value: dict
        """
        # In some cases, the incoming value may already be a value object.
        # For example, when running a dict through the Applicant Filter, the `loan` attribute will already be a
        #   LoanObject.
        # :see: applicant_journey.filters.Applicant
        return value if isinstance(value, self.vo_type) else self.vo_type(value or {})

    def merge(self, existing, incoming):
        """
        Merges one value object into another.

        :type existing: applicant_journey.value_object.base.BaseValueObject
        :type incoming: applicant_journey.value_object.base.BaseValueObject
        """
        # To keep things simple, we will just modify `existing` in place (that's what `BaseValueObject.update` does
        #   anyway).
        if existing is None:
            return incoming

        if incoming is not None:
            existing.update(incoming)

        return existing

    def hydrate(self, value):
        """
        Hydrates an incoming dict into a value object.

        :type value: dict
        """
        # Do not return a value object instance here; the field's `init` method will get invoked later on.
        return self.vo_type.hydrate_values(value or {})

    def dehydrate(self, value):
        """
        Dehydrates a value object into a dict.

        :type value: applicant_journey.value_object.base.BaseValueObject
        """
        return None if value is None else value.dehydrate()

    def make_public_value(self, value):
        """
        Returns the "public" version of a value object.

        :type value: applicant_journey.value_object.base.BaseValueObject
        """
        fields = tuple(self.public) if isinstance(self.public, set) else ()

        return None if value is None else value.get_public_values(*fields)


class Bytes(Field):
    """
    A field that stores a byte string.

    Note:  The field assumes that its value is encoded using UTF-8 by default!
    """
    def __init__(self, key=None, encoding='utf-8'):
        super(Bytes, self).__init__(key)

        self.encoding = encoding

    def hydrate(self, value):
        return None if value is None else value.encode(self.encoding)

    def dehydrate(self, value):
        # Convert the value into a unicode for serialization.
        return None if value is None else value.decode(self.encoding)


class Date(Field):
    """
    A field that contains a date object.
    """
    def hydrate(self, value):
        return None if value is None else datetime.strptime(value, '%Y-%m-%d').date()

    def dehydrate(self, value):
        """
        :type value: datetime.date
        """
        return None if value is None else value.strftime('%Y-%m-%d')

    def make_public_value(self, value):
        """
        :type value: datetime.date
        """
        return None if value is None else value.isoformat()


class Datetime(Field):
    """
    A field that contains a datetime object.
    """
    def hydrate(self, value):
        return None if value is None else datetime.strptime(value, '%Y-%m-%d %H:%M:%S').replace(tzinfo=utc)

    def dehydrate(self, value):
        """
        :type value: datetime
        """
        return None if value is None else value.strftime('%Y-%m-%d %H:%M:%S')

    def make_public_value(self, value):
        """
        :type value: datetime
        """
        return None if value is None else value.isoformat()


class Decimal(Field):
    """
    A field that contains a decimal.Decimal object.
    """
    def hydrate(self, value):
        return None if value is None else DecimalType(value)

    def dehydrate(self, value):
        return None if value is None else format(value, 'f')

    def make_public_value(self, value):
        # :see: importer.core.filters.simple.Unicode#_apply
        return None if value is None else format(value, 'f')
