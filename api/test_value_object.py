# coding=utf-8
from __future__ import absolute_import, unicode_literals

from datetime import date, datetime
from decimal import Decimal
from django.test import TestCase

from pytz import utc
from api.value_object import fields
from api.value_object.base import BaseValueObject


class SimpleTestValueObject(BaseValueObject):
    name            = fields.Primitive()
    age             = fields.Primitive()

    # Note that this field's attribute name is different than its dict key.
    # This becomes important later.
    favorite_color  = fields.Primitive('favoriteColor')

class SimpleValueObjectTestCase(TestCase):
    """
    Value object tests covering very simple use cases.
    """
    def test_construct(self):
        """
        Each value object declares its own fields.
        """
        obj = SimpleTestValueObject({
            'name':             'Lancelot',
            'age':              34,
            'favoriteColor':    'blue',
        })

        # The internal representation of the value object generally matches the init values.
        self.assertEqual(obj.name, 'Lancelot')
        self.assertEqual(obj.age, 34)
        # Note the attribute name is different than the dict key.
        # :see: SimpleTestValueObject.favorite_color
        self.assertEqual(obj.favorite_color, 'blue')

        # The public representation of the value object is often different than the init values, but not in this case.
        self.assertDictEqual(obj.get_public_values(), {
            'name':             'Lancelot',
            'age':              34,
            'favoriteColor':    'blue',
        })

    def test_construct_nulls(self):
        """
        The value object is initialized with null values.
        """
        obj = SimpleTestValueObject({
            'name':             None,
            'age':              None,
            'favoriteColor':    None,
        })

        # As you'd expect....
        self.assertIsNone(obj.name)
        self.assertIsNone(obj.age)
        self.assertIsNone(obj.favorite_color)

        self.assertDictEqual(obj.get_public_values(), {
            'name':             None,
            'age':              None,
            'favoriteColor':    None,
        })

    def test_dehydrate(self):
        """
        Dehydrating a value object into a serializable form.
        """
        obj = SimpleTestValueObject({
            'name':             'Galahad',
            'age':              35,
            'favoriteColor':    'yellow',
        })

        # Not too interesting... yet.
        self.assertDictEqual(obj.dehydrate(), {
            'name':             'Galahad',
            'age':              35,
            'favoriteColor':    'yellow',
        })

    def test_dehydrate_nulls(self):
        """
        Dehydrating a value object that is full of nulls.
        """
        obj = SimpleTestValueObject({
            'name':             None,
            'age':              None,
            'favoriteColor':    None,
        })

        self.assertDictEqual(obj.dehydrate(), {
            'name':             None,
            'age':              None,
            'favoriteColor':    None,
        })

    def test_hydrate(self):
        """
        Reconstructing a value object from its dehydrated data.
        """
        obj = SimpleTestValueObject.hydrate({
            'name':             'Robin',
            'age':              39,
            'favoriteColor':    'yellow',
        })

        # So far, still pretty boring.  It'll get more interesting soon.
        self.assertIsInstance(obj, SimpleTestValueObject)
        self.assertEqual(obj.name, 'Robin')
        self.assertEqual(obj.age, 39)
        self.assertEqual(obj.favorite_color, 'yellow')

    def test_hydrate_nulls(self):
        """
        Reconstructing a value object from a collection of nulls.
        """
        obj = SimpleTestValueObject.hydrate({
            'name':             None,
            'age':              None,
            'favoriteColor':    None,
        })

        self.assertIsInstance(obj, SimpleTestValueObject)
        self.assertIsNone(obj.name)
        self.assertIsNone(obj.age)
        self.assertIsNone(obj.favorite_color)

    def test_update(self):
        """
        Updating the values of one value object from another.
        """
        obj = SimpleTestValueObject({
            'name':             'Arthur',
            'age':              42,
            'favoriteColor':    'white',
        })

        obj.update(SimpleTestValueObject({
            'name':             'Old Man',
            'age':              92,
            'favoriteColor':    'black',
        }))

        self.assertEqual(obj.name, 'Old Man')
        self.assertEqual(obj.age, 92)
        self.assertEqual(obj.favorite_color, 'black')

    def test_update_existing_nulls(self):
        """
        Updating a value object full of nulls from a value object that contains non-null values.
        """
        obj = SimpleTestValueObject({
            'name':             None,
            'age':              None,
            'favoriteColor':    None,
        })

        obj.update(SimpleTestValueObject({
            'name':             'Bedevere',
            'age':              44,
            'favoriteColor':    'gray',
        }))

        self.assertEqual(obj.name, 'Bedevere')
        self.assertEqual(obj.age, 44)
        self.assertEqual(obj.favorite_color, 'gray')

    def test_update_incoming_nulls(self):
        """
        Update a value object with a value object full of nulls.
        """
        obj = SimpleTestValueObject({
            'name':             'Not-Appearing-in-This-Film',
            'age':              -1,
            'favoriteColor':    '???',
        })

        obj.update(SimpleTestValueObject({
            'name':             None,
            'age':              None,
            'favoriteColor':    None,
        }))

        # Incoming null values get ignored when updating a value object.
        self.assertEqual(obj.name, 'Not-Appearing-in-This-Film')
        self.assertEqual(obj.age, -1)
        self.assertEqual(obj.favorite_color, '???')


class TypedTestValueObject(BaseValueObject):
    bytes       = fields.Bytes()
    date        = fields.Date()
    datetime    = fields.Datetime()
    decimal     = fields.Decimal()

class TypedFieldsValueObjectTestCase(TestCase):
    """
    Value object tests covering use cases involving fields with more complex behavior.
    """
    def test_construct(self):
        """
        Each field has its own way of internally representing values.
        """
        obj = TypedTestValueObject({
            'bytes':    b'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n',
            'date':     date(2015, 9, 22),
            'datetime': datetime(2015, 9, 22, 17, 58, 36, tzinfo=utc),
            'decimal':  Decimal('2.6E-2'),
        })

        #
        # The internal representation of the value object matches the init values.
        self.assertEqual(obj.bytes, b'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n')
        self.assertEqual(obj.date, date(2015, 9, 22))
        self.assertEqual(obj.datetime, datetime(2015, 9, 22, 17, 58, 36, tzinfo=utc))
        self.assertEqual(obj.decimal, Decimal('2.6E-2'))

        #
        # However, the public representation of the value object is a bit different.
        self.assertDictEqual(obj.get_public_values(), {
            'bytes':    'Iñtërnâtiônàlizætiøn',
            'date':     '2015-09-22',
            'datetime': '2015-09-22T17:58:36+00:00',
            'decimal':  '0.026',
        })

    def test_construct_nulls(self):
        """
        Each field has its own way of handling null values.
        """
        obj = TypedTestValueObject({
            'bytes':    None,
            'date':     None,
            'datetime': None,
            'decimal':  None,
        })

        # Simple enough, right?
        # Things get a wee bit more complicated when we start working with more complex field types, but for now, it's
        #   pretty straightforward.
        self.assertIsNone(obj.bytes)
        self.assertIsNone(obj.date)
        self.assertIsNone(obj.datetime)
        self.assertIsNone(obj.decimal)

        self.assertDictEqual(obj.get_public_values(), {
            'bytes':    None,
            'date':     None,
            'datetime': None,
            'decimal':  None,
        })

    def test_dehydrate(self):
        """
        Each field has its own dehydration behavior.
        """
        obj = TypedTestValueObject({
            'bytes':    b'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n',
            'date':     date(2015, 9, 22),
            'datetime': datetime(2015, 9, 22, 17, 58, 36, tzinfo=utc),
            'decimal':  Decimal('2.6E-2'),
        })

        self.assertDictEqual(obj.dehydrate(), {
            'bytes':    'Iñtërnâtiônàlizætiøn',
            'date':     '2015-09-22',
            'datetime': '2015-09-22 17:58:36',
            'decimal':  '0.026',
        })

    def test_dehydrate_nulls(self):
        """
        Dehydrating a value object with typed fields that contain null values.
        """
        obj = TypedTestValueObject({
            'bytes':    None,
            'date':     None,
            'datetime': None,
            'decimal':  None,
        })

        self.assertDictEqual(obj.dehydrate(), {
            'bytes':    None,
            'date':     None,
            'datetime': None,
            'decimal':  None,
        })

    def test_hydrate(self):
        """
        Each field has its own hydration behavior.
        """
        obj = TypedTestValueObject.hydrate({
            'bytes':    'Iñtërnâtiônàlizætiøn',
            'date':     '2015-09-22',
            'datetime': '2015-09-22 17:58:36',
            'decimal':  '0.026',
        })

        self.assertIsInstance(obj, TypedTestValueObject)

        self.assertEqual(obj.bytes, b'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n')
        self.assertEqual(obj.date, date(2015, 9, 22))
        self.assertEqual(obj.datetime, datetime(2015, 9, 22, 17, 58, 36, tzinfo=utc))
        self.assertEqual(obj.decimal, Decimal('0.026'))

    def test_hydrate_nulls(self):
        """
        Hydrating a value object with typed fields containing null values.
        """
        obj = TypedTestValueObject.hydrate({
            'bytes':    None,
            'date':     None,
            'datetime': None,
            'decimal':  None,
        })

        self.assertIsNone(obj.bytes)
        self.assertIsNone(obj.date)
        self.assertIsNone(obj.datetime)
        self.assertIsNone(obj.decimal)

    def test_update(self):
        """
        Each field has its own update behavior.
        """
        obj = TypedTestValueObject({
            'bytes':    b'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n',
            'date':     date(2015, 9, 22),
            'datetime': datetime(2015, 9, 22, 17, 58, 36, tzinfo=utc),
            'decimal':  Decimal('2.6E-2'),
        })

        obj.update(TypedTestValueObject({
            'bytes':    b'I18n',
            'date':     date(2012, 4, 6),
            'datetime': datetime(1972, 7, 30, 6, 0, 1, tzinfo=utc),
            'decimal':  Decimal('42'),
        }))

        self.assertEqual(obj.bytes, b'I18n')
        self.assertEqual(obj.date, date(2012, 4, 6))
        self.assertEqual(obj.datetime, datetime(1972, 7, 30, 6, 0, 1, tzinfo=utc))
        self.assertEqual(obj.decimal, Decimal('42'))

    def test_update_existing_nulls(self):
        """
        A value object with typed fields containing null values is updated from a value object with non-null values.
        """
        obj = TypedTestValueObject({
            'bytes':    None,
            'date':     None,
            'datetime': None,
            'decimal':  None,
        })

        obj.update(TypedTestValueObject({
            'bytes':    b'I18n',
            'date':     date(2012, 4, 6),
            'datetime': datetime(1972, 7, 30, 6, 0, 1, tzinfo=utc),
            'decimal':  Decimal('42'),
        }))

        self.assertEqual(obj.bytes, b'I18n')
        self.assertEqual(obj.date, date(2012, 4, 6))
        self.assertEqual(obj.datetime, datetime(1972, 7, 30, 6, 0, 1, tzinfo=utc))
        self.assertEqual(obj.decimal, Decimal('42'))

    def test_update_incoming_nulls(self):
        """
        A value object with typed fields containing non-null values is updated from a value object with null values.
        """
        obj = TypedTestValueObject({
            'bytes':    b'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n',
            'date':     date(2015, 9, 22),
            'datetime': datetime(2015, 9, 22, 17, 58, 36, tzinfo=utc),
            'decimal':  Decimal('2.6E-2'),
        })

        obj.update(TypedTestValueObject({
            'bytes':    None,
            'date':     None,
            'datetime': None,
            'decimal':  None,
        }))

        self.assertEqual(obj.bytes, b'I\xc3\xb1t\xc3\xabrn\xc3\xa2ti\xc3\xb4n\xc3\xa0liz\xc3\xa6ti\xc3\xb8n')
        self.assertEqual(obj.date, date(2015, 9, 22))
        self.assertEqual(obj.datetime, datetime(2015, 9, 22, 17, 58, 36, tzinfo=utc))
        self.assertEqual(obj.decimal, Decimal('2.6E-2'))


class ComplexTestValueObject(BaseValueObject):
    simple  = fields.Collection(key='simpleCollection')
    dates   = fields.Collection(fields.Date, key='dateCollection')

class ComplexFieldsValueObjectTestCase(TestCase):
    """
    Value object tests covering field types that contain collections of values.
    """
    def test_construct(self):
        """
        Complex fields store their values as collections of some kind.
        """
        obj = ComplexTestValueObject({
            'simpleCollection': {
                'a':    'Apple',
                'j':    'Jacks',
                'c':    'Cinnamon-Toasted',
            },

            'dateCollection':   {
                'TMP':  date(1979, 12, 7),
                'WOK':  date(1982, 6, 4),
                'S4S':  date(1984, 6, 1),
            },
        })

        # Internally, complex fields store their values as collections.
        self.assertDictEqual(obj.simple, {
            'a':    'Apple',
            'j':    'Jacks',
            'c':    'Cinnamon-Toasted',
        })

        self.assertDictEqual(obj.dates, {
            'TMP':  date(1979, 12, 7),
            'WOK':  date(1982, 6, 4),
            'S4S':  date(1984, 6, 1),
        })

        # Complex fields delegate public value generation to their sub-field.
        self.assertDictEqual(obj.get_public_values(), {
            'simpleCollection': {
                'a':    'Apple',
                'j':    'Jacks',
                'c':    'Cinnamon-Toasted',
            },

            'dateCollection':   {
                'TMP':  '1979-12-07',
                'WOK':  '1982-06-04',
                'S4S':  '1984-06-01',
            },
        })

    def test_construct_nulls(self):
        """
        A value object with complex fields is initialized with null values.
        """
        obj = ComplexTestValueObject({
            'simpleCollection': None,
            'dateCollection':   None,
        })

        # Note that the resulting attribute values are empty dicts, not `None`.
        # Note also that this means we don't have to write any other null-handling tests for these field types (:
        self.assertDictEqual(obj.simple, {})
        self.assertDictEqual(obj.dates, {})

        self.assertDictEqual(obj.get_public_values(), {
            'simpleCollection': {},
            'dateCollection':   {},
        })

    def test_dehydrate(self):
        """
        Complex fields generate their own objects when the value object is dehydrated.
        """
        obj = ComplexTestValueObject({
            'simpleCollection': {
                'a':    'Apple',
                'j':    'Jacks',
                'c':    'Cinnamon-Toasted',
            },

            'dateCollection':   {
                'TMP':  date(1979, 12, 7),
                'WOK':  date(1982, 6, 4),
                'S4S':  date(1984, 6, 1),
            },
        })

        self.assertDictEqual(obj.dehydrate(), {
            'simpleCollection': {
                'a':    'Apple',
                'j':    'Jacks',
                'c':    'Cinnamon-Toasted',
            },

            # Each value in the collection gets dehydrated individually.
            'dateCollection':   {
                'TMP':  '1979-12-07',
                'WOK':  '1982-06-04',
                'S4S':  '1984-06-01',
            },
        })

    def test_hydrate(self):
        """
        Complex fields generate their own objects when re-hydrating values.
        """
        obj = ComplexTestValueObject.hydrate({
            'simpleCollection': {
                'foo':  'bar',
                'baz':  'luhrmann',
            },

            'dateCollection':   {
                'VH':   '1986-11-26',
                'FF':   '1989-06-09',
                'UC':   '1991-12-06',
            },
        })

        self.assertIsInstance(obj, ComplexTestValueObject)

        self.assertDictEqual(obj.simple, {
            'foo':  'bar',
            'baz':  'luhrmann',
        })

        self.assertDictEqual(obj.dates, {
            'VH':   date(1986, 11, 26),
            'FF':   date(1989, 6, 9),
            'UC':   date(1991, 12, 6),
        })

    def test_update(self):
        """
        Complex fields perform a merge operation when updating their values.
        """
        obj = ComplexTestValueObject({
            'simpleCollection': {
                'red':      'green',
                'yellow':   'purple',
                'blue':     'orange',
            },

            'dateCollection': {
                'G':        date(1994, 11, 18),
                'FC':       date(1996, 11, 22),
                'I':        date(1998, 12, 11),
            },
        })

        obj.update(ComplexTestValueObject({
            'simpleCollection': {
                'yellow':   'magenta',
                'blue':     'teal',
                'white':    'black',
            },

            'dateCollection': {
                'FC':       date(2009, 4, 7),
                'I':        date(2013, 4, 23),
                'N':        date(2016, 7, 22),
            },
        }))

        self.assertDictEqual(obj.simple, {
            # Value in obj1 but not obj2: left alone.
            'red':      'green',

            # Values in both: obj2 overwrites obj1.
            'yellow':   'magenta',
            'blue':     'teal',

            # Value in obj2 but not obj1: added.
            'white':    'black',
        })

        self.assertDictEqual(obj.dates, {
            'G':        date(1994, 11, 18),
            'FC':       date(2009, 4, 7),
            'I':        date(2013, 4, 23),
            'N':        date(2016, 7, 22),
        })


class TestLoanObject(BaseValueObject):
    amount      = fields.Primitive()

class TestAddressObject(BaseValueObject):
    street      = fields.Primitive()

class TestApplicantObject(BaseValueObject):
    name        = fields.Primitive()
    loan        = fields.ValueObject(TestLoanObject)
    """:type: TestLoanObject"""
    # You knew this was coming.
    addresses   = fields.Collection(TestAddressObject)
    """:type: dict[unicode, TestAddressObject]"""

class NestedValueObjectTestCase(TestCase):
    """
    The most complex (and common) use cases for value objects:  Value objects that contain other value objects.
    """
    def test_construct(self):
        """
        Building a value object with nested field types.
        """
        obj = TestApplicantObject({
            'name': 'Marcus',
            'loan': {
                'amount':   10000,
            },

            'addresses': {
                'home':     {
                    'street':   '740 Evergreen Terrace',
                },

                'work':     {
                    'street':   '112½ Beacon Street',
                }
            },
        })

        self.assertEqual(obj.name, 'Marcus')

        self.assertIsInstance(obj.loan, TestLoanObject)
        self.assertEqual(obj.loan.amount, 10000)

        self.assertIsInstance(obj.addresses['home'], TestAddressObject)
        self.assertEqual(obj.addresses['home'].street, '740 Evergreen Terrace')

        self.assertIsInstance(obj.addresses['work'], TestAddressObject)
        self.assertEqual(obj.addresses['work'].street, '112½ Beacon Street')

        # A value objects public form includes the public forms of its nested value objects.
        self.assertDictEqual(obj.get_public_values(), {
            'name': 'Marcus',
            'loan': {
                'amount':   10000,
            },

            'addresses': {
                'home':     {
                    'street':   '740 Evergreen Terrace',
                },

                'work':     {
                    'street':   '112½ Beacon Street',
                },
            },
        })

    def test_construct_nulls(self):
        """
        Building a value object with nested field types using null values.
        """
        obj = TestApplicantObject({
            'name':         None,
            'loan':         None,
            'addresses':    None,
        })

        self.assertIsNone(obj.name)
        self.assertDictEqual(obj.addresses, {})

        self.assertIsInstance(obj.loan, TestLoanObject)
        self.assertIsNone(obj.loan.amount)

        self.assertDictEqual(obj.get_public_values(), {
            'name':         None,
            'loan':         {
                'amount':       None,
            },
            'addresses':    {},
        })

    def test_dehydrate(self):
        """
        Dehydrating a value object that contains other value objects.
        """
        obj = TestApplicantObject({
            'name': 'Marcus',
            'loan': {
                'amount':   10000,
            },

            'addresses': {
                'home':     {
                    'street':   '740 Evergreen Terrace',
                },

                'work':     {
                    'street':   '112½ Beacon Street',
                }
            },
        })

        self.assertDictEqual(obj.dehydrate(), {
            'name': 'Marcus',
            'loan': {
                'amount':   10000,
            },

            'addresses': {
                'home':     {
                    'street':   '740 Evergreen Terrace',
                },

                'work':     {
                    'street':   '112½ Beacon Street',
                },
            },
        })

    def test_hydrate(self):
        """
        Hydrating a value object that contains other value objects.
        """
        obj = TestApplicantObject.hydrate({
            'name': 'Marcus',
            'loan': {
                'amount':   10000,
            },

            'addresses': {
                'home':     {
                    'street':   '740 Evergreen Terrace',
                },

                'work':     {
                    'street':   '112½ Beacon Street',
                },
            },
        })

        self.assertIsInstance(obj, TestApplicantObject)

        self.assertEqual(obj.name, 'Marcus')

        self.assertIsInstance(obj.loan, TestLoanObject)
        self.assertEqual(obj.loan.amount, 10000)

        self.assertIsInstance(obj.addresses['home'], TestAddressObject)
        self.assertEqual(obj.addresses['home'].street, '740 Evergreen Terrace')

        self.assertIsInstance(obj.addresses['work'], TestAddressObject)
        self.assertEqual(obj.addresses['work'].street, '112½ Beacon Street')

    def test_update(self):
        """
        Merging two value objects that each contain other value objects.
        """
        obj = TestApplicantObject({
            'name': 'Marcus',
            'loan': {
                'amount':   10000,
            },

            'addresses': {
                'home':     {
                    'street':   '740 Evergreen Terrace',
                },

                'work':     {
                    'street':   '112½ Beacon Street',
                }
            },
        })

        obj.update(TestApplicantObject({
            'name': 'Indiana',
            'loan': {
                'amount':   20000,
            },

            'addresses': {
                'work':     {
                    'street':   '221B Baker Street',
                },

                'branch':   {
                    'street':   '12 Grimmauld Place',
                },
            },
        }))

        self.assertEqual(obj.name, 'Indiana')

        self.assertIsInstance(obj.loan, TestLoanObject)
        self.assertEqual(obj.loan.amount, 20000)

        # Address in obj1 but not obj2: leave alone.
        self.assertIsInstance(obj.addresses['home'], TestAddressObject)
        self.assertEqual(obj.addresses['home'].street, '740 Evergreen Terrace')

        # !!! This part's really important !!!

        # Address in obj1 and obj2: MERGE.
        self.assertIsInstance(obj.addresses['work'], TestAddressObject)
        self.assertEqual(obj.addresses['work'].street, '221B Baker Street')

        # Address in obj2 but not obj1:  ADD.
        self.assertIsInstance(obj.addresses['branch'], TestAddressObject)
        self.assertEqual(obj.addresses['branch'].street, '12 Grimmauld Place')


class PartialVisibilitySimpleTestValueObject(BaseValueObject):
    public1             = fields.Primitive()
    public2             = fields.Primitive()
    private             = fields.Primitive(public=False)

class PartialVisibilityComplexTestValueObject(BaseValueObject):
    public_collection   = fields.Collection(key='publicCollection')
    private_collection  = fields.Collection(key='privateCollection', public=False)
    partial_collection  = fields.Collection(key='partialCollection', public={'alpha', 'charlie', 'delta'})

    public_nested       = fields.ValueObject(PartialVisibilitySimpleTestValueObject, key='publicNested')
    """:type: PartialVisibilitySimpleTestValueObject"""
    private_nested      = fields.ValueObject(PartialVisibilitySimpleTestValueObject, key='privateNested', public=False)
    """:type: PartialVisibilitySimpleTestValueObject"""
    partial_nested      = fields.ValueObject(
        vo_type = PartialVisibilitySimpleTestValueObject,
        key     = 'partialNested',
        public  = {'public1', 'private', 'foo'},
    )
    """:type: PartialVisibilitySimpleTestValueObject"""

class FieldVisibilityTestCase(TestCase):
    """
    Field visibility tests for value objects.
    """
    def test_all_fields(self):
        """
        By default, fields marked as private do not appear in the value object's public values.
        """
        obj = PartialVisibilityComplexTestValueObject({
            'publicCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            'privateCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            'partialCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            'publicNested': {
                'public1':  'foo',
                'public2':  'bar',
                'private':  'baz',
            },

            'privateNested': {
                'public1':  'foo',
                'public2':  'bar',
                'private':  'baz',
            },

            'partialNested': {
                'public1':  'foo',
                'public2':  'bar',
                'private':  'baz',
            },
        })

        # Internally, both public and private values are available.
        self.assertDictEqual(obj.public_collection, {
            'alpha':    1,
            'bravo':    2,
            'charlie':  3,
        })

        self.assertDictEqual(obj.private_collection, {
            'alpha':    1,
            'bravo':    2,
            'charlie':  3,
        })

        self.assertDictEqual(obj.partial_collection, {
            'alpha':    1,
            'bravo':    2,
            'charlie':  3,
        })

        self.assertIsInstance(obj.public_nested, PartialVisibilitySimpleTestValueObject)
        self.assertEqual(obj.public_nested.public1, 'foo')
        self.assertEqual(obj.public_nested.public2, 'bar')
        self.assertEqual(obj.public_nested.private, 'baz')

        self.assertIsInstance(obj.private_nested, PartialVisibilitySimpleTestValueObject)
        self.assertEqual(obj.private_nested.public1, 'foo')
        self.assertEqual(obj.private_nested.public2, 'bar')
        self.assertEqual(obj.private_nested.private, 'baz')

        self.assertIsInstance(obj.partial_nested, PartialVisibilitySimpleTestValueObject)
        self.assertEqual(obj.partial_nested.public1, 'foo')
        self.assertEqual(obj.partial_nested.public2, 'bar')
        self.assertEqual(obj.partial_nested.private, 'baz')

        # However, when getting the public version of the value object, private values are omitted.
        self.assertDictEqual(obj.get_public_values(), {
            # When `public=True`, all values in the collection are included.
            'publicCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            # When `public` is a container, only matching keys are included.
            'partialCollection': {
                'alpha':    1,
                'charlie':  3,
            },

            # Similar rules apply to nested value objects.
            'publicNested': {
                'public1':  'foo',
                'public2':  'bar',
            },

            # `partial_nested` is configured only to include certain fields (but note that private fields in the
            #   nested object are still excluded, even if explicitly listed in the parent field's configuration).
            'partialNested': {
                'public1':  'foo',
            },
        })

    def test_specify_fields(self):
        """
        You can specify which PUBLIC fields you want to include in the result.

        Note that private fields will not be included, even if explicitly specified.
        """
        obj = PartialVisibilityComplexTestValueObject({
            'publicCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            'privateCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            'partialCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            'publicNested': {
                'public1':  'foo',
                'public2':  'bar',
                'private':  'baz',
            },

            'privateNested': {
                'public1':  'foo',
                'public2':  'bar',
                'private':  'baz',
            },

            'partialNested': {
                'public1':  'foo',
                'public2':  'bar',
                'private':  'baz',
            },
        })

        self.assertDictEqual(obj.get_public_values('publicCollection', 'publicNested', 'privateCollection'), {
            'publicCollection': {
                'alpha':    1,
                'bravo':    2,
                'charlie':  3,
            },

            'publicNested': {
                'public1':  'foo',
                'public2':  'bar',
            },

            # Note that `privateCollection` is not included in the result because it is private.
        })

        # Note that you must specify field keys, not attribute values!
        self.assertDictEqual(
            obj.get_public_values('public_collection', 'public_nested', 'private_collection'),
            {},
        )