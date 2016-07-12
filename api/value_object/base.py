# coding=utf-8
from __future__ import absolute_import, unicode_literals, print_function

from six import with_metaclass

from api.value_object.fields import Field


class ValueObjectMeta(type):
    """
    Transforms value object classes from human-readable (compile time) to computer-friendly (runtime).
    """
    fields = None
    """:type: dict[str, Value]"""

    @staticmethod
    def __new__(mcs, name, bases, attrs):
        """
        :type name:     str
        :type bases:    tuple[type]
        :type attrs:    dict
        """
        attrs['fields'] = {}

        # Move fields to a special container.
        # Note that we iterate over a pre-computed list so that we can modify `attrs` from inside the loop.
        for attr in [attr for attr, field in attrs.items() if isinstance(field, Field)]:
            field = attrs.pop(attr)

            #
            # If no dict key is specified, assign the attribute name.
            # E.g.:
            #   name = fields.Primitive() => fields.Primitive(key=b'name')
            #
            if not field.key:
                field.key = attr

            attrs['fields'][attr] = field

        return super(ValueObjectMeta, mcs).__new__(mcs, name, bases, attrs)

    def hydrate(cls, dehydrated):
        """
        Reconstructs a value object from dehydrated values.

        :type dehydrated: dict

        :rtype: BaseValueObject
        """
        return cls(cls.hydrate_values(dehydrated or {}))

    def hydrate_values(cls, dehydrated):
        """
        Hydrates dehydrated values without constructing a value object.

        :type dehydrated: dict

        :rtype: dict
        """
        return {
            field.key or name: field.hydrate(dehydrated.get(field.key or name))
                for name, field in cls.fields.items()
        }


class BaseValueObject(with_metaclass(ValueObjectMeta)):
    """
    Base functionality for value objects.
    """
    def __init__(self, filtered_data):
        super(BaseValueObject, self).__init__()

        self._fields = type(self).fields
        self._values = {
            name: field.init(filtered_data.get(field.key, None))
                for name, field in self._fields.items()
        }

    def __getattr__(self, attr):
        try:
            return self._values[attr]
        except KeyError:
            raise AttributeError('{type!r} object has no attribute {attr!r}'.format(
                type    = type(self).__name__,
                attr    = attr,
            ))

    def update(self, incoming):
        """
        Updates a value object from another value object of the same type.  Incoming null values will be ignored.

        :type incoming: BaseValueObject
        """
        self._values.update({
            name: field.merge(self._values.get(name), incoming._values.get(name))
                for name, field in self._fields.items()
        })

    def dehydrate(self):
        """
        Serializes the value object into a form that can be stored in other contexts (e.g., cache, database, etc.).

        Note that this value is not intended to be included in API responses nor other contexts where an end user might
            see it; use `get_public_values` for that.

        :rtype: dict

        :see: get_public_values
        """
        return {
            field.key: field.dehydrate(self._values.get(name))
                for name, field in self._fields.items()
        }

    def get_public_values(self, *fields):
        """
        Returns a dict containing the "public" version of the value object's values.

        Public values may be different than the internally-stored values (or even omitted altogether), depending on
            the field type.

        Unlike `dehydrate`, the value returned by this method is intended to be used in API responses and other contexts
            where an end user might see it.

        :type fields: tuple[basestring]
        :param fields: If desired, you may specify the fields you want included (by default, all fields are included).
            Note:       Use field keys here, not attribute values.
            Note also:  Private fields will not be included in the result, even if explicitly listed here.

        :rtype: dict
        """
        public_fields = set(self.get_public_field_keys(*fields))

        return {
            field.key: field.make_public_value(self._values.get(name))
                for name, field in self._fields.items()
                if field.key in public_fields
        }

    def get_public_field_keys(self, *fields):
        """
        Returns the keys of the fields in this value object that are public.

        :type fields: tuple[basestring]
        :param fields: If desired, you may specify the fields you want included (by default, all fields are included).
            Note:       Use field keys here, not attribute values.
            Note also:  Private fields will not be included in the result, even if explicitly listed here.

        :rtype: tuple(basestring)
        """
        return tuple(
            field.key
                for field in self._fields.values()
                if ((not fields) or (field.key in fields)) and field.public
        )