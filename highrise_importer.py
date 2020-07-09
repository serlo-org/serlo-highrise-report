"""Imports contact informations from Highrise into a local database."""

import os
import sys
import xml.etree.ElementTree as ET

import requests

from serlo.model import SerloDatabase, Email, PhoneNumber, Person, UnitType, \
                        WorkingUnit, Tag

TOKEN_VARIABLE = "HIGHRISE_API_TOKEN"

PROJECT_ID = "6436430"
SUPPORT_UNIT_ID = "4849968"
MENTORING_DEAL_ID = "6438903"
MEMBER_ID = "5360080"
SUBJECT_DATA_OVERVIEW = "1224165"
SUBJECT_DATA_STORAGE = "1258882"
SUBJECT_DATA_SLACK = "1311275"

def xml_text(xml):
    """Returns the inner text of the XML element `xml`. In case it doesn't
    contain an inner text an empty string is returned."""
    if xml is None:
        raise TypeError("xml_text(): XML argument must not be 'None'")

    return str.join('', xml.itertext())

def xml_find(tag_name, xml):
    """Returns the child with tag `tag_name` of the XML element `xml`. It
    throws an `AssertationError` when no or more than one children of the tag
    `tag_name` are defined."""
    if xml is None:
        raise TypeError("xml_text(): XML argument must not be 'None'")

    results = xml.findall(tag_name)

    assert results, f"Child with tag `{tag_name}` not found."
    assert len(results) < 2, f"Too many children with tag `{tag_name}` found."

    return results[0]

def parse_subject_datas(xml):
    """Returns a dircectory of all subject data in `xml`. Subject data are
    values stored in custom fields in Highrise. This functions returns
    a directoy with all custom field values as strings. The keys are
    links."""
    subject_datas = xml.find("subject_datas")

    if subject_datas:
        return dict((xml_text(xml_find("subject_field_id", child)),
                     xml_text(xml_find("value", child))) for child
                    in subject_datas.findall("subject_data"))

    return dict()

def parse_email(xml):
    """Parse emails defined by XML specification `xml`."""
    return Email(address=xml_text(xml_find("address", xml)),
                 location=xml_text(xml_find("location", xml)))

def parse_phone_number(xml):
    """Parse phone number defined by XML specification `xml`."""
    return PhoneNumber(number=xml_text(xml_find("number", xml)),
                       location=xml_text(xml_find("location", xml)))

def parse_tag(xml):
    """Parse tag defined by XML specification `xml`."""
    return Tag(tag_id=int(xml_text(xml_find("id", xml))))

def parse_person(xml):
    """Parse person defined by XML specification `xml`."""
    contact_data = xml_find("contact-data", xml)

    return (xml_text(xml_find("id", xml)),
            Person(first_name=xml_text(xml_find("first-name", xml)),
                   last_name=xml_text(xml_find("last-name", xml)),
                   emails=[parse_email(e) for e in
                           xml_find("email-addresses", contact_data)],
                   phone_numbers=[parse_phone_number(e) for e in
                                  xml_find("phone-numbers", contact_data)],
                   tags=[parse_tag(e) for e in xml_find("tags", xml)]))

def parse_people(xml):
    """Parse people defined by XML specification `xml`."""
    return [parse_person(e) for e in xml.findall("person", xml)]

def parse_working_unit(xml, persons):
    """Parse a working unit defined by XML specification `xml`."""
    category_id = xml_text(xml_find("category-id", xml))

    if category_id == PROJECT_ID:
        unit_type = UnitType.project
    elif category_id == SUPPORT_UNIT_ID:
        unit_type = UnitType.support_unit
    else:
        return None

    if xml_text(xml_find("status", xml)) != "pending":
        return None

    subject_datas = parse_subject_datas(xml)

    overview_document = subject_datas.get(SUBJECT_DATA_OVERVIEW, "")
    storage_url = subject_datas.get(SUBJECT_DATA_STORAGE, "")
    slack_url = subject_datas.get(SUBJECT_DATA_SLACK, "")

    try:
        person_responsible = persons[xml_text(xml_find("party-id", xml))]
    except KeyError:
        # TODO: write unittests for this exception
        return None

    participant_ids = [xml_text(xml_find("id", x)) for x
                       in xml_find("parties", xml)]

    return WorkingUnit(name=xml_text(xml_find("name", xml)),
                       description=xml_text(xml_find("background", xml)),
                       overview_document=overview_document,
                       storage_url=storage_url,
                       slack_url=slack_url,
                       unit_type=unit_type,
                       person_responsible=person_responsible,
                       participants=[persons[x] for x in participant_ids
                                     if x in persons])

def parse_working_units(xml, persons):
    """Parse working units from a XML specification."""
    results = [parse_working_unit(x, persons) for x in xml]

    return [x for x in results if x is not None]

def parse_mentoring(xml):
    """Returns a dictionary specifing all mentoring relationships. The key is
    the person id of mentor and the value is a list of all person ids which
    are the mentees."""
    result = []

    for deal in xml:
        if xml_text(xml_find("category-id", deal)) == MENTORING_DEAL_ID:
            result.append((xml_text(xml_find("party-id", deal)),
                           [xml_text(xml_find("id", party)) for
                            party in xml_find("parties", deal)]))

    return dict(result)

def api_call(endpoint, api_token, params=None):
    """Executes an API call to Highrise."""
    if params is None:
        params = {}

    url = f"https://de-serlo.highrisehq.com/{endpoint}.xml"
    req = requests.get(url, auth=(api_token, "_"), params=params)

    return ET.fromstring(req.text)

def run_script():
    """Executes this script."""
    try:
        database_file = sys.argv[1]
    except IndexError:
        sys.exit("Error: No database file specified as first argument.")

    try:
        api_token = os.environ[TOKEN_VARIABLE]
    except KeyError:
        sys.exit(f"Error: Environment Variable {TOKEN_VARIABLE} not defined.")

    database = SerloDatabase(database_file)

    persons = dict(parse_people(api_call("people", api_token,
                                         params={"tag_id": MEMBER_ID})))

    deals = api_call("deals", api_token)

    mentoring_spec = parse_mentoring(deals)

    for mentor_id, mentee_ids in mentoring_spec.items():
        for mentee_id in mentee_ids:
            mentor = persons.get(mentor_id, None)
            mentee = persons.get(mentee_id, None)

            if mentor and mentee:
                mentee.mentor = mentor

    units = parse_working_units(deals, persons)

    database.add_all(persons.values())
    database.add_all(units)

if __name__ == "__main__":
    run_script()
