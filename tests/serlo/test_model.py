"""Tests for the modul `serlo.model`."""

from unittest import TestCase

from serlo.model import UnitType, Email, Person, PhoneNumber, SerloDatabase, \
                        WorkingUnit, Tag
from tests.data import generate_persons, generate_emails, \
                       generate_working_units, generate_phone_numbers, \
                       generate_tags

class TestEmail(TestCase):
    """Testcases for the model `Email`."""

    def setUp(self):
        self.email1 = Email(address="hello@example.org", location="Work")
        self.email2 = Email(address="", location="Home")
        self.email3 = Email(address="not-an-email", location="")

    def test_attr_tablename(self):
        """Testcase for attribute `Email.__tablename__`."""
        self.assertEqual(Email.__tablename__, "email")

    def test_attr_id(self):
        """Testcase for attribute `Email.id`."""
        self.assertIsNone(self.email1.id)
        self.assertIsNone(self.email2.id)
        self.assertIsNone(self.email3.id)

    def test_attr_address(self):
        """Testcase for attribute `Email.address`."""
        self.assertEqual(self.email1.address, "hello@example.org")
        self.assertEqual(self.email2.address, "")
        self.assertEqual(self.email3.address, "not-an-email")

    def test_attr_location(self):
        """Testcase for attribute `Email.location`."""
        self.assertEqual(self.email1.location, "Work")
        self.assertEqual(self.email2.location, "Home")
        self.assertEqual(self.email3.location, "")

class TestPhoneNumber(TestCase):
    """Testcases for the model `PhoneNumber`."""

    def setUp(self):
        self.number1 = PhoneNumber(number="+49017867", location="Work")
        self.number2 = PhoneNumber(number="0178645389", location="Mobile")
        self.number3 = PhoneNumber(number="", location="")

    def test_attr_tablename(self):
        """Testcase for attribute `__tablename__`."""
        self.assertEqual(PhoneNumber.__tablename__, "phonenumber")

    def test_attr_id(self):
        """Testcase for attribute `PhoneNumber.id`."""
        self.assertIsNone(self.number1.id)
        self.assertIsNone(self.number2.id)
        self.assertIsNone(self.number3.id)

    def test_attr_number(self):
        """Testcase for attribute `PhoneNumber.number`."""
        self.assertEqual(self.number1.number, "+49017867")
        self.assertEqual(self.number2.number, "0178645389")
        self.assertEqual(self.number3.number, "")

    def test_attr_location(self):
        """Testcase for attribute `PhoneNumber.location`."""
        self.assertEqual(self.number1.location, "Work")
        self.assertEqual(self.number2.location, "Mobile")
        self.assertEqual(self.number3.location, "")

class TestTag(TestCase):
    """Testcase for model `Tag`."""

    def setUp(self):
        self.tag1 = Tag(tag_id=42)
        self.tag2 = Tag(tag_id=23)

    def test_attr_tag_id(self):
        """Testcase for attribute `tag_id`."""
        self.assertEqual(self.tag1.tag_id, 42)
        self.assertEqual(self.tag2.tag_id, 23)

class TestPerson(TestCase):
    """Testcases for model `Person`."""
    # pylint: disable=too-many-instance-attributes

    def setUp(self):
        self.person1, self.person2, self.person3 = generate_persons()
        self.email1, self.email2, self.email3 = generate_emails()
        self.phone1, self.phone2, self.phone3 = generate_phone_numbers()
        self.tag1, self.tag2, self.tag3 = generate_tags()

    def test_attr_id(self):
        """Testcase for attribute `Person.id`."""
        self.assertIsNone(self.person1.id)
        self.assertIsNone(self.person2.id)

    def test_attr_tablename(self):
        """Testcase for attribute `Person.__tablename__`."""
        self.assertEqual(Person.__tablename__, "person")

    def test_attr_first_name(self):
        """Testcase for attribute `Person.first_name`."""
        self.assertEqual(self.person1.first_name, "Markus")
        self.assertEqual(self.person2.first_name, "Yannick")
        self.assertEqual(self.person3.first_name, "")

    def test_attr_emails(self):
        """Testcase for attribute `Person.emails`."""
        self.assertListEqual(self.person1.emails, [self.email1])
        self.assertListEqual(self.person2.emails, [self.email2, self.email3])
        self.assertListEqual(self.person3.emails, [])

    def test_attr_phone_numbers(self):
        """Testcase for attribute `Person.phone_numbers`."""
        self.assertListEqual(self.person1.phone_numbers, [self.phone1])
        self.assertListEqual(self.person2.phone_numbers,
                             [self.phone2, self.phone3])
        self.assertListEqual(self.person3.phone_numbers, [])

    def test_attr_tags(self):
        """Testcase for attribute `Person.tags`."""
        self.assertListEqual(self.person1.tags,
                             [self.tag1, self.tag2, self.tag3])
        self.assertListEqual(self.person2.tags, [self.tag2])
        self.assertListEqual(self.person3.tags, [])

    def test_attr_last_name(self):
        """Testcase for attribute `Person.last_name`."""
        self.assertEqual(self.person1.last_name, "Miller")
        self.assertEqual(self.person2.last_name, "Müller")
        self.assertEqual(self.person3.last_name, "")

    def test_attr_name(self):
        """Testcase for attribute `Person.name`."""
        self.assertEqual(self.person1.name, "Markus Miller (Pause, Intern)")
        self.assertEqual(self.person2.name, "Yannick Müller (Intern)")
        self.assertEqual(self.person3.name, " ")

    def test_attr_work_emails(self):
        """Testcase for attribute `Person.work_emails`."""
        self.assertListEqual(self.person1.work_emails, [])
        self.assertListEqual(self.person2.work_emails, [self.email2])
        self.assertListEqual(self.person3.work_emails, [])

    def test_attr_work_phone_numbers(self):
        """Testcase for attribute `Person.work_phone_numbers`."""
        self.assertListEqual(self.person1.work_phone_numbers, [])
        self.assertListEqual(self.person2.work_phone_numbers, [self.phone2])
        self.assertListEqual(self.person3.work_phone_numbers, [])

    def test_attr_mentor(self):
        """Testcase for attribute `Person.mentor`."""
        self.assertEqual(self.person1.mentor, self.person2)
        self.assertEqual(self.person2.mentor, self.person3)
        self.assertIsNone(self.person3.mentor)

    def test_has_tag(self):
        """Testcase for the method `Person.has_tag()`."""
        self.assertTrue(self.person1.has_tag(self.tag1.tag_id))
        self.assertTrue(self.person1.has_tag(self.tag2.tag_id))
        self.assertTrue(self.person2.has_tag(self.tag2.tag_id))

        self.assertFalse(self.person3.has_tag(self.tag3.tag_id))
        self.assertFalse(self.person2.has_tag(self.tag3.tag_id))

class TestUnitType(TestCase):
    """Testcases for the class `UnitType`."""

    def test_attr_abbreviation(self):
        """Testcase for attribute `UnitType.abbreviation`."""
        self.assertEqual(UnitType.project.abbreviation, "P")
        self.assertEqual(UnitType.support_unit.abbreviation, "U")

class TestWorkingUnit(TestCase):
    """Testcases for the class `WorkingUnit`."""

    def setUp(self):
        self.project1, self.project2, \
                self.unit1, self.unit2 = generate_working_units()

        self.person1, self.person2, self.person3 = generate_persons()

    def test_attr_tablename(self):
        """Test for attribute `WorkingUnit.__tablename__`."""
        self.assertEqual(WorkingUnit.__tablename__, "workingunit")

    def test_attr_id(self):
        """Test for attribute `WorkingUnit.id`"""
        self.assertIsNone(self.project1.id)
        self.assertIsNone(self.unit1.id)

    def test_attr_name(self):
        """Test for attribute `WorkingUnit.name`."""
        self.assertEqual(self.project1.name, "project1")
        self.assertEqual(self.project2.name, "")
        self.assertEqual(self.unit1.name, "Support Unit Master")
        self.assertEqual(self.unit2.name, "Another support unit")

    def test_attr_description(self):
        """Test for attribute `WorkingUnit.description`."""
        self.assertEqual(self.project1.description, "My description")
        self.assertEqual(self.project2.description, "")
        self.assertEqual(self.unit1.description, "A cool unit.")
        self.assertEqual(self.unit2.description, "Hello World")

    def test_attr_person_responsible(self): # pylint: disable=invalid-name
        """Test for attribute `WorkingUnit.person_responsible`."""
        self.assertEqual(self.project1.person_responsible, self.person1)
        self.assertEqual(self.project2.person_responsible, self.person2)
        self.assertEqual(self.unit1.person_responsible, self.person1)
        self.assertEqual(self.unit2.person_responsible, self.person3)

    def test_attr_participants(self):
        """Test for attribute `WorkingUnit.participants`."""
        self.assertListEqual(self.project1.participants, [self.person3])
        self.assertListEqual(self.project2.participants, [])
        self.assertListEqual(self.unit1.participants, [self.person2])
        self.assertListEqual(self.unit2.participants,
                             [self.person1, self.person2])

    def test_attr_members(self):
        """Test for attribute `WorkingUnit.members`."""
        self.assertListEqual(self.project1.members,
                             [self.person1, self.person3])
        self.assertListEqual(self.project2.members, [self.person2])
        self.assertListEqual(self.unit1.members, [self.person1, self.person2])
        self.assertListEqual(self.unit2.members,
                             [self.person3, self.person1, self.person2])

    def test_attr_unit_type(self): # pylint: disable=invalid-name
        """Test for attribute `WorkingUnit.type`."""
        self.assertEqual(self.project1.unit_type, UnitType.project)
        self.assertEqual(self.project2.unit_type, UnitType.project)
        self.assertEqual(self.unit1.unit_type, UnitType.support_unit)
        self.assertEqual(self.unit2.unit_type, UnitType.support_unit)

    def test_attr_overview_document(self): # pylint: disable=invalid-name
        """Test for attribute `WorkingUnit.overview_document`"""
        self.assertEqual(self.project1.overview_document, "overview_document")
        self.assertEqual(self.project2.overview_document, "")
        self.assertEqual(self.unit1.overview_document, "http://example.org")
        self.assertEqual(self.unit2.overview_document, "Hello Document")

    def test_attr_storage_url(self): # pylint: disable=invalid-name
        """Test for attribute `WorkingUnit.storage_url`"""
        self.assertEqual(self.project1.storage_url, "storage_url")
        self.assertEqual(self.project2.storage_url, "")
        self.assertEqual(self.unit1.storage_url, "https://example.com/url/")
        self.assertEqual(self.unit2.storage_url, "")


    def test_attr_title(self):
        """Test for attribute `WorkingUnit.title`."""
        self.assertEqual(self.project1.title, "P - project1")
        self.assertEqual(self.project2.title, "P - ")
        self.assertEqual(self.unit1.title, "U - Support Unit Master")
        self.assertEqual(self.unit2.title, "U - Another support unit")


class TestSerloDatabase(TestCase):
    """Testcases for the class `SerloDatabase`."""
    # pylint: disable=too-many-instance-attributes

    def setUp(self):
        self.database = SerloDatabase("sqlite:///:memory:")
        self.person1, self.person2, self.person3 = generate_persons()[0:3]

        self.persons = [self.person1, self.person2, self.person3]

        self.project1, self.project2, \
                self.unit1, self.unit2 = generate_working_units()[0:4]

        self.units = [self.project1, self.project2, self.unit1, self.unit2]

    def test_storing_nothing(self):
        """Testcase when nothing is stored."""
        self.assertListEqual(list(self.database.persons), [])
        self.assertListEqual(list(self.database.working_units), [])

        self.database.add_all([])

        self.assertListEqual(list(self.database.persons), [])
        self.assertListEqual(list(self.database.working_units), [])

    def test_attr_persons(self):
        """Testcase for storing persons to `SerloDatabase`."""
        self.database.add_all(self.persons)

        self.assertSetEqual(set(self.database.persons), set(self.persons))

    def test_attr_working_units(self):
        """Testcase for storing working units to `SerloDatabase`."""
        self.database.add_all([self.project2, self.project1])
        self.database.add_all([self.unit1, self.unit2])

        self.assertSetEqual(set(self.database.working_units), set(self.units))

    def test_attr_projects(self):
        """Testcase for accessing all active projects."""
        self.database.add_all([self.project1, self.project2, self.unit1,
                               self.unit2])

        self.assertSetEqual(set(self.database.projects),
                            set([self.project1, self.project2]))

    def test_attr_support_units(self):
        """Testcase for accessing all active support_units."""
        self.database.add_all([self.project1, self.project2, self.unit1,
                               self.unit2])

        self.assertSetEqual(set(self.database.support_units),
                            set([self.unit1, self.unit2]))

    def test_attr_managing_units(self):
        """Test for attribute `Person.managing_unit`."""
        self.database.add_all([self.project1, self.project2, self.unit1,
                               self.unit2])

        person1 = self.project1.person_responsible
        person3 = self.unit2.person_responsible

        self.assertEqual(list(person1.managing_units),
                         [self.project1, self.unit1])
        self.assertEqual(list(person3.managing_units), [self.unit2])

    def test_attr_participating_units(self): # pylint: disable=invalid-name
        """Test for attribute `Person.participating_unit`."""
        self.database.add_all([self.project1, self.project2, self.unit1,
                               self.unit2])

        person1 = self.project1.person_responsible
        person2 = self.project2.person_responsible

        self.assertEqual(set(person1.participating_units), set([self.unit2]))
        self.assertEqual(set(person2.participating_units),
                         set([self.unit1, self.unit2]))

    def test_attr_mentees(self):
        """Test for attribute `Person.mentees`."""
        self.database.add_all([self.person1, self.person2, self.person3])

        self.assertListEqual(self.person1.mentees, [])
        self.assertListEqual(self.person2.mentees, [self.person1])
        self.assertListEqual(self.person3.mentees, [self.person2])
